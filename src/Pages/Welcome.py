from tkinter import ttk


class WelcomePage(ttk.Frame):
    def __init__(self: object, parent: object) -> ttk.Frame:
        super().__init__(parent)

        ttk.Label(self, text='Welcome to Cypher', style='big.TLabel').place(
            relx=.5, rely=.5, anchor='c')
