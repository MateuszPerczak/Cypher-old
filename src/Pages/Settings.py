from tkinter import ttk, PhotoImage, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfile


class SettingsPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        # content
        ttk.Label(self, text='Settings').pack(
            fill='x', padx=10, pady=(10, 5))

        Theme(self, props['theme']).pack(fill='x', padx=10, pady=(0, 10))
        Export(self, props).pack(fill='x', padx=10, pady=(0, 10))
        About(self, props['theme']).pack(fill='x', padx=10, pady=(0, 10))


class Theme(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable
        self.theme = theme
        self.selected_theme: StringVar = StringVar(
            value=theme.get_internal_theme())

        self.icon_cache = {
            'brush': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\brush.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\brush.png')
            },
        }

        theme_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        self.header: ttk.Label = ttk.Label(theme_panel, image=self.icon_cache['brush'][self.theme.get_theme(
        )], text='Theme', style='dark.TLabel', compound='left')
        self.header.pack(side='left', anchor='center', fill='y')
        ttk.Radiobutton(theme_panel, text='System', style='small.TRadiobutton', value='System', command=lambda: self.theme.apply(
            'Dark'), variable=self.selected_theme).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Light', style='small.TRadiobutton', value='Light', command=lambda: self.theme.apply(
            'Light'), variable=self.selected_theme).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Dark', style='small.TRadiobutton', value='Dark', command=lambda: self.theme.apply(
            'Dark'), variable=self.selected_theme).pack(side='right', anchor='center', padx=(0, 10))
        theme_panel.pack(side='top', fill='x', pady=10, padx=10)
        # bind theme change
        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        self.header.configure(
            image=self.icon_cache['brush'][self.theme.get_theme()])


class About(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable
        self.theme = theme
        self.icon_cache = {
            'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\info.png'),
            'Light': PhotoImage(file=r'Resources\\Icons\\Light\\info.png')
        }

        self.header: ttk.Label = ttk.Label(self, image=self.icon_cache[self.theme.get_theme(
        )], text='About Cypher', style='dark.TLabel', compound='left')
        self.header.pack(side='top', fill='x', padx=10, pady=10)
        ttk.Label(self, text='Version: 1.2.5 Build: 170222',
                  style='small.dark.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text='Author: Mateusz Perczak',
                  style='small.dark.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text='Icons: Icons8', style='small.dark.TLabel').pack(
            side='top', fill='x', padx=10, pady=(0, 10))
        # bind theme change
        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        self.header.configure(image=self.icon_cache[self.theme.get_theme()])


class Export(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # variables
        self._protector: object = props['protector']
        self.theme: object = props['theme']

        self.icon_cache = {
            'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\identity.png'),
            'Light': PhotoImage(file=r'Resources\\Icons\\Light\\identity.png')
        }
        # content
        content_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        self.header: ttk.Label = ttk.Label(content_panel, image=self.icon_cache[self.theme.get_theme(
        )], text='Identity', style='dark.TLabel', compound='left')
        self.header.pack(side='left', anchor='center', fill='y')

        ttk.Button(content_panel, text='Export', style='center.TButton',
                   command=self._export_identity).pack(side='right')
        ttk.Button(content_panel, text='Import', style='center.TButton',
                   command=self._import_identity).pack(side='right')

        content_panel.pack(side='top', fill='x', pady=10, padx=10)

        # bind theme change
        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        self.header.configure(image=self.icon_cache[self.theme.get_theme()])

    def _export_identity(self: object) -> None:
        _file: object = asksaveasfile(mode='wb', defaultextension='.idt', filetypes=[
                                      ('Identity file', '.idt')])
        if _file:
            _file.write(self._protector.export_identity())
            _file.close()

    def _import_identity(self: object) -> None:
        _identity_file: str = askopenfilename(
            filetypes=[('Identity files', '*.idt')], title='Select identity file')
        self._protector.import_identity(_identity_file)
