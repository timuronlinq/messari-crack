import tkinter.filedialog as filedialog
import customtkinter as ctk
from utils.helpers import Theme


class SelectorPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            **kwargs,
        )

        self.lbl_target = ctk.CTkLabel(
            self,
            text="TARGET:  MESSARI",
            font=(Theme.FONT_FAMILY, 13, "bold"),
            text_color=Theme.NEON_PRIMARY,
            anchor="w",
        )
        self.lbl_target.pack(fill="x", padx=18, pady=(14, 10))

        self.lbl_path = ctk.CTkLabel(
            self,
            text="INSTALLATION  PATH",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            text_color=Theme.NEON_ACCENT,
            anchor="w",
        )
        self.lbl_path.pack(fill="x", padx=18, pady=(2, 4))

        self.path_row = ctk.CTkFrame(self, fg_color="transparent")
        self.path_row.pack(fill="x", padx=18, pady=(0, 14))

        self.entry_path = ctk.CTkEntry(
            self.path_row,
            height=34,
            font=(Theme.FONT_FAMILY, 11),
            fg_color=Theme.BG_INPUT,
            border_color=Theme.BORDER_DIM,
            border_width=1,
            text_color=Theme.TEXT_PRIMARY,
            placeholder_text="C:\\Program Files\\Messari\\...",
            placeholder_text_color=Theme.TEXT_DIM,
            corner_radius=10,
        )
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_browse = ctk.CTkButton(
            self.path_row,
            text="\U0001f4c2",
            width=38,
            height=34,
            font=(Theme.FONT_FAMILY, 14),
            fg_color=Theme.BG_INPUT,
            hover_color=Theme.NEON_PRIMARY,
            text_color=Theme.NEON_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER_DIM,
            corner_radius=10,
            command=self._browse_folder,
        )
        self.btn_browse.pack(side="right")

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Select target directory")
        if folder:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder)
