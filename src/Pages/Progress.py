from tkinter import ttk


class ProgressPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        self.maximum: int = 0
        center_panel: ttk.Frame = ttk.Frame(self)
        ttk.Label(center_panel, text='Encrypting...').pack(side='top')
        self.progress_label: ttk.Label = ttk.Label(center_panel, text='0%',
                                                   style='small.TLabel')
        self.progress_label.pack(side='top')
        self.progressbar: ttk.Progressbar = ttk.Progressbar(center_panel)
        self.progressbar.pack(side='top', fill='x')
        self.done_button: ttk.Button = ttk.Button(
            center_panel, text='Done', style='center.TButton', command=self.__end_progress)
        self.done_button.state(['disabled'])
        self.done_button.pack(side='top', pady=10)
        center_panel.place(relx=.5, rely=.5, anchor='c', relwidth=.5)

    def set_progress(self: object, value: int) -> None:
        self.progressbar.configure(value=value)
        self.progress_label.config(
            text=f'{int((value * 100) / self.maximum)}%')
        if value >= self.maximum:
            self.done_button.state(['!disabled'])

    def set_max_value(self: object, value: int) -> None:
        self.maximum = value
        self.progressbar.configure(maximum=value)

    def __end_progress(self: object) -> None:
        self.maximum = 0
        self.progressbar.configure(value=0)
        self.progress_label.config(text='0%')
        self.done_button.state(['disabled'])
        self.lower()
