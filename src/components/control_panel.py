import customtkinter as ctk
from utils.helpers import Theme


class ControlPanel(ctk.CTkFrame):

    def __init__(self, master, on_execute=None, on_copy=None, on_close=None, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)

        self._on_execute = on_execute
        self._on_copy = on_copy
        self._on_close = on_close

        self.btn_execute = ctk.CTkButton(
            self,
            text="\u26a1  EXECUTE  PATCH",
            font=(Theme.FONT_FAMILY, 15, "bold"),
            height=46,
            width=360,
            fg_color=Theme.NEON_PRIMARY,
            hover_color=Theme.NEON_SECONDARY,
            text_color=Theme.BUTTON_FG,
            text_color_disabled=Theme.TEXT_DIM,
            corner_radius=12,
            border_width=2,
            border_color=Theme.NEON_PRIMARY,
            command=self._handle_execute,
        )
        self.btn_execute.pack(pady=(8, 10))

        self.progress = ctk.CTkProgressBar(
            self,
            width=380,
            height=14,
            fg_color=Theme.PROGRESS_BG,
            progress_color=Theme.NEON_PRIMARY,
            corner_radius=7,
            border_width=1,
            border_color=Theme.BORDER_DIM,
        )
        self.progress.set(0)
        self.progress.pack(pady=(0, 4))

        self.lbl_status = ctk.CTkLabel(
            self,
            text="IDLE \u2014 waiting for command",
            font=(Theme.FONT_FAMILY, 10),
            text_color=Theme.TEXT_DIM,
        )
        self.lbl_status.pack(pady=(0, 6))

        self.bottom_row = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_row.pack(fill="x", padx=30, pady=(2, 0))

        self.btn_copy = ctk.CTkButton(
            self.bottom_row,
            text="\U0001f4cb  Copy Log",
            font=(Theme.FONT_FAMILY, 11),
            width=130,
            height=32,
            fg_color=Theme.BG_CARD,
            hover_color=Theme.NEON_PRIMARY,
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            corner_radius=10,
            command=self._handle_copy,
        )
        self.btn_copy.pack(side="left", expand=True, padx=4)

        self.btn_close = ctk.CTkButton(
            self.bottom_row,
            text="\u2715  Close",
            font=(Theme.FONT_FAMILY, 11),
            width=130,
            height=32,
            fg_color=Theme.BG_CARD,
            hover_color=Theme.NEON_RED,
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            corner_radius=10,
            command=self._handle_close,
        )
        self.btn_close.pack(side="right", expand=True, padx=4)

    def _handle_execute(self):
        if self._on_execute:
            self._on_execute()

    def _handle_copy(self):
        if self._on_copy:
            self._on_copy()

    def _handle_close(self):
        if self._on_close:
            self._on_close()

    def set_running(self, running: bool):
        if running:
            self.btn_execute.configure(
                state="disabled",
                fg_color=Theme.BG_CARD,
                border_color=Theme.TEXT_DIM,
                text="\u23f3  PATCHING...",
            )
            self.lbl_status.configure(
                text="RUNNING \u2014 do not close",
                text_color=Theme.NEON_YELLOW,
            )
        else:
            self.btn_execute.configure(
                state="normal",
                fg_color=Theme.NEON_PRIMARY,
                border_color=Theme.NEON_PRIMARY,
                text="\u26a1  EXECUTE  PATCH",
            )

    def set_progress(self, value: float):
        self.progress.set(value)
        if value < 0.5:
            self.progress.configure(progress_color=Theme.NEON_PRIMARY)
        elif value < 0.85:
            self.progress.configure(progress_color=Theme.NEON_SECONDARY)
        else:
            self.progress.configure(progress_color=Theme.NEON_YELLOW)

    def set_error(self):
        self.lbl_status.configure(
            text="\u2718  PATCH FAILED \u2014 FATAL ERROR",
            text_color=Theme.NEON_RED,
        )
        self.progress.configure(progress_color=Theme.NEON_RED)
