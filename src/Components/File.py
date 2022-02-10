from tkinter import ttk, PhotoImage
from os.path import basename, getsize
from Components.Converter import sizeof_fmt


class FilePanel(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # variables
        theme = props['theme']
        self.file: str = props['file']
        self.files: list = props['files']
        self.icon_cache = props['icon_cache']

        self.icon: ttk.Label = ttk.Label(self, image=self.icon_cache['file'][theme.get_theme(
        )], style='dark.TLabel')
        self.icon.pack(side='left', ipady=5, padx=(5, 0))

        info_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        ttk.Label(info_panel, text=basename(self.file),
                  style='small.dark.TLabel').pack(side='top', fill='x', pady=(5, 0))
        ttk.Label(info_panel, text=sizeof_fmt(getsize(self.file)),
                  style='small.dark.TLabel').pack(side='top', fill='x', pady=(0, 5))
        info_panel.pack(side='left')

        self.remove_button: ttk.Button = ttk.Button(
            self, image=self.icon_cache['delete'][theme.get_theme()], command=self.remove_self)
        self.remove_button.pack(side='right', padx=(0, 5), anchor='c')

        theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: object) -> None:
        self.icon.configure(image=self.icon_cache['file'][theme])
        self.remove_button.configure(image=self.icon_cache['delete'][theme])

    def remove_self(self: object) -> None:
        self.files.remove(self.file)
        self.destroy()
