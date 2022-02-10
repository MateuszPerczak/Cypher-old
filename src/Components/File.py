from tkinter import ttk
from os.path import basename, getsize
from Components.Converter import sizeof_fmt


class EncryptionFile(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # variables
        self.theme = props['theme']
        self.file: str = props['file']
        self.files: list = props['files']
        self.icon_cache = props['icon_cache']

        self.icon: ttk.Label = ttk.Label(self, image=self.icon_cache['file'][self.theme.get_theme(
        )], style='dark.TLabel')
        self.icon.pack(side='left', ipady=5, padx=(5, 0))

        info_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        ttk.Label(info_panel, text=basename(self.file),
                  style='small.dark.TLabel').pack(side='top', fill='x', pady=(5, 0))
        ttk.Label(info_panel, text=sizeof_fmt(getsize(self.file)),
                  style='small.dark.TLabel').pack(side='top', fill='x', pady=(0, 5))
        info_panel.pack(side='left')

        self.remove_button: ttk.Button = ttk.Button(
            self, image=self.icon_cache['delete'][self.theme.get_theme()], command=self.remove_self)
        self.remove_button.pack(side='right', padx=(0, 5), anchor='c')

        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        self.icon.configure(
            image=self.icon_cache['file'][self.theme.get_theme()])
        self.remove_button.configure(
            image=self.icon_cache['delete'][self.theme.get_theme()])

    def remove_self(self: object) -> None:
        self.files.remove(self.file)
        self.theme.unbind(self.__on_theme_changed)
        self.destroy()


class DecryptionFile(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # variables
        self.theme = props['theme']
        self.file: str = props['file']
        self.icon_cache = props['icon_cache']
        self.state: str = 'encrypted'

        self.icon: ttk.Label = ttk.Label(self, image=self.icon_cache['file'][self.theme.get_theme(
        )], style='dark.TLabel')
        self.icon.pack(side='left', ipady=5, padx=(5, 0))

        info_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        ttk.Label(info_panel, text=basename(self.file),
                  style='small.dark.TLabel').pack(side='top', fill='x', pady=(5, 0))
        ttk.Label(info_panel, text=sizeof_fmt(getsize(self.file)),
                  style='small.dark.TLabel').pack(side='top', fill='x', pady=(0, 5))
        info_panel.pack(side='left')

        self.status_label: ttk.Label = ttk.Label(
            self, image=self.icon_cache['encrypt'][self.theme.get_theme()], style='dark.TLabel')
        self.status_label.pack(side='right', padx=(0, 5), anchor='c')

        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        if self.state == 'encrypted':
            self.status_label.configure(
                image=self.icon_cache['encrypt'][self.theme.get_theme()])
        else:
            self.status_label.configure(
                image=self.icon_cache['decrypt'][self.theme.get_theme()])
        self.icon.configure(
            image=self.icon_cache['file'][self.theme.get_theme()])

    def set_decrypt(self: object) -> None:
        self.state = 'decrypted'
        self.status_label.configure(
            image=self.icon_cache['decrypt'][self.theme.get_theme()])

    def remove_self(self: object) -> None:
        self.theme.unbind(self.__on_theme_changed)
        self.destroy()
