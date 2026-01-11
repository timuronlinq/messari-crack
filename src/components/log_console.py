import customtkinter as ctk
from utils.helpers import Theme


class LogConsole(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            **kwargs,
        )

        self.lbl_title = ctk.CTkLabel(
            self,
            text="\u25b8  PATCH  LOG",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.NEON_SECONDARY,
            anchor="w",
        )
        self.lbl_title.pack(fill="x", padx=14, pady=(8, 2))

        self.textbox = ctk.CTkTextbox(
            self,
            font=(Theme.FONT_FAMILY, 11),
            fg_color=Theme.BG_DARKEST,
            text_color=Theme.TEXT_LOG,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            wrap="word",
            activate_scrollbars=True,
            scrollbar_button_color=Theme.NEON_PRIMARY,
            scrollbar_button_hover_color=Theme.NEON_SECONDARY,
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        self._show_placeholder()

    def _show_placeholder(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "  Awaiting command...\n")
        self.textbox.insert("end", "  Press EXECUTE PATCH to start.\n")
        self.textbox.configure(state="disabled")

    def clear(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

    def append_line(self, text: str):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def append_error(self, text: str):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text + "\n")
        self.textbox.see("end")
        self.textbox.configure(text_color=Theme.NEON_RED)
        self.textbox.configure(state="disabled")

    def reset_color(self):
        self.textbox.configure(text_color=Theme.TEXT_LOG)

    def get_all_text(self) -> str:
        self.textbox.configure(state="normal")
        content = self.textbox.get("1.0", "end").strip()
        self.textbox.configure(state="disabled")
        return content
