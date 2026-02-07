import customtkinter as ctk
from utils.helpers import Theme


class HeaderPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Theme.BG_DARKEST, corner_radius=0, **kwargs)

        self.title_label = ctk.CTkLabel(
            self,
            text="⚙  MSR CRACK  v5.0 — 2026",
            font=(Theme.FONT_FAMILY, 17, "bold"),
            text_color=Theme.NEON_PRIMARY,
        )
        self.title_label.pack(pady=(14, 2))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="[ RESEARCH  HUB  SUBSCRIPTION  BYPASS ]",
            font=(Theme.FONT_FAMILY, 10),
            text_color=Theme.NEON_SECONDARY,
        )
        self.subtitle_label.pack(pady=(0, 6))

        self.separator = ctk.CTkFrame(self, height=2, fg_color=Theme.NEON_PRIMARY, corner_radius=0)
        self.separator.pack(fill="x", padx=24, pady=(0, 4))

        self._glow_state = True
        self._animate_glow()

    def _animate_glow(self):
        if self._glow_state:
            self.title_label.configure(text_color=Theme.GLOW_ALT)
        else:
            self.title_label.configure(text_color=Theme.NEON_PRIMARY)
        self._glow_state = not self._glow_state
        self.after(900, self._animate_glow)
