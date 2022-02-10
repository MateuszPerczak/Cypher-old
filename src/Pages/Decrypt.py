from tkinter import ttk


class DecryptPage(ttk.Frame):
    def __init__(self: object, parent: object) -> ttk.Frame:
        super().__init__(parent)
        # content
        ttk.Label(self, text='Decrypt').pack(
            fill='x', padx=10, pady=10)
