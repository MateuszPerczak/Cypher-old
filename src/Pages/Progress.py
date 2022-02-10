from tkinter import ttk


class ProgressPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)

        theme: str = props['theme']

    def start_progress(self: object) -> None:
        pass
