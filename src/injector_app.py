import threading
import time
import customtkinter as ctk

from components import HeaderPanel, SelectorPanel, ControlPanel, LogConsole
from utils.helpers import (
    Theme, get_phase_logs, get_error_logs,
    random_delay, FINAL_ERROR_BANNER,
)


class InjectorApp(ctk.CTk):

    WIN_WIDTH = 720
    WIN_HEIGHT = 660

    def __init__(self):
        super().__init__()

        self.title("MSR Crack v5.0")
        self.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG_DARKEST)

        try:
            self.attributes("-topmost", True)
        except Exception:
            pass

        self._running = False
        self._build_ui()

    def _build_ui(self):
        self.header = HeaderPanel(self)
        self.header.pack(fill="x")

        self.top_row = ctk.CTkFrame(self, fg_color="transparent")
        self.top_row.pack(fill="x", padx=14, pady=(6, 4))

        self.selector = SelectorPanel(self.top_row)
        self.selector.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.info_frame = ctk.CTkFrame(
            self.top_row,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            width=240,
        )
        self.info_frame.pack(side="right", fill="y")
        self.info_frame.pack_propagate(False)

        info_lines = [
            ("ENGINE", "MesBreak™ v5.0.1"),
            ("MODE", "Deep Hook (Ring-0)"),
            ("ARCH", "x86_64 / ARM64"),
            ("BUILD", "2026.02.01-release"),
            ("PROXY", "HTTP/2 tunnel — active"),
        ]
        lbl_header = ctk.CTkLabel(
            self.info_frame,
            text="SYSTEM  INFO",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.NEON_SECONDARY,
            anchor="w",
        )
        lbl_header.pack(fill="x", padx=14, pady=(12, 6))

        for key, val in info_lines:
            row = ctk.CTkFrame(self.info_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=2)
            ctk.CTkLabel(
                row, text=f"{key}:", width=55, anchor="w",
                font=(Theme.FONT_FAMILY, 10, "bold"),
                text_color=Theme.TEXT_DIM,
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=val, anchor="w",
                font=(Theme.FONT_FAMILY, 10),
                text_color=Theme.NEON_PRIMARY,
            ).pack(side="left", padx=(4, 0))

        self.log_console = LogConsole(self)
        self.log_console.pack(fill="both", expand=True, padx=14, pady=(4, 4))

        self.control = ControlPanel(
            self,
            on_execute=self._start_injection,
            on_copy=self._copy_log,
            on_close=self._close_app,
        )
        self.control.pack(fill="x", padx=14, pady=(0, 10))

    def _start_injection(self):
        if self._running:
            return

        self._running = True
        self.control.set_running(True)
        self.control.set_progress(0)
        self.log_console.reset_color()
        self.log_console.clear()

        thread = threading.Thread(target=self._worker, daemon=True)
        thread.start()

    def _worker(self):
        phases = get_phase_logs()
        error_lines = get_error_logs()
        total_lines = sum(len(p) for p in phases) + len(error_lines)
        current_line = 0

        for phase in phases:
            for line in phase:
                time.sleep(random_delay(0.2, 0.55))
                current_line += 1
                progress = current_line / total_lines
                self.after(0, self.log_console.append_line, line)
                self.after(0, self.control.set_progress, progress)
            time.sleep(0.35)

        time.sleep(0.6)

        for line in error_lines:
            time.sleep(random_delay(0.3, 0.7))
            current_line += 1
            progress = current_line / total_lines
            self.after(0, self.log_console.append_line, line)
            self.after(0, self.control.set_progress, progress)

        time.sleep(0.5)
        self.after(0, self.control.set_progress, 1.0)
        self.after(0, self.log_console.append_error, FINAL_ERROR_BANNER)
        self.after(0, self.control.set_error)
        self.after(0, self._finish)

    def _finish(self):
        self._running = False
        self.control.set_running(False)
        self.control.btn_execute.configure(text="\U0001f501  RETRY")

    def _copy_log(self):
        text = self.log_console.get_all_text()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.control.btn_copy.configure(
                text="\u2714 Copied!",
                fg_color=Theme.NEON_ACCENT,
                text_color=Theme.BG_DARKEST,
            )
            self.after(1500, lambda: self.control.btn_copy.configure(
                text="\U0001f4cb  Copy Log",
                fg_color=Theme.BG_CARD,
                text_color=Theme.TEXT_PRIMARY,
            ))

    def _close_app(self):
        self.destroy()
