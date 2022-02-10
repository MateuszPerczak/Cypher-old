from tkinter import ttk, PhotoImage, StringVar


class SettingsPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        # content
        ttk.Label(self, text='Settings').pack(
            fill='x', padx=10, pady=(10, 5))

        Theme(self, props['theme']).pack(fill='x', padx=10, pady=(0, 10))
        About(self, props['theme']).pack(fill='x', padx=10, pady=(0, 10))


class Theme(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable
        self.theme: StringVar = StringVar(value=theme.get_internal_theme())

        self.icon_cache = {
            'brush': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\brush.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\brush.png')
            },
        }

        theme_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        self.header: ttk.Label = ttk.Label(theme_panel, image=self.icon_cache['brush'][theme.get_theme(
        )], text='Theme', style='dark.TLabel', compound='left')
        self.header.pack(side='left', anchor='center', fill='y')
        ttk.Radiobutton(theme_panel, text='System', style='small.TRadiobutton', value='System', command=lambda: theme.apply(
            'Dark'), variable=self.theme).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Light', style='small.TRadiobutton', value='Light', command=lambda: theme.apply(
            'Light'), variable=self.theme).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Dark', style='small.TRadiobutton', value='Dark', command=lambda: theme.apply(
            'Dark'), variable=self.theme).pack(side='right', anchor='center', padx=(0, 10))
        theme_panel.pack(side='top', fill='x', pady=10, padx=10)
        # bind theme change
        theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: object) -> None:
        self.header.configure(image=self.icon_cache['brush'][theme])


class About(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable

        self.icon_cache = {
            'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\info.png'),
            'Light': PhotoImage(file=r'Resources\\Icons\\Light\\info.png')
        }

        self.header: ttk.Label = ttk.Label(self, image=self.icon_cache[theme.get_theme(
        )], text='About Cypher', style='dark.TLabel', compound='left')
        self.header.pack(side='top', fill='x', padx=10, pady=10)
        ttk.Label(self, text='Version: 1.0.0 Build: 090222',
                  style='small.dark.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text='Author: Mateusz Perczak',
                  style='small.dark.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text='Icons: Icons8', style='small.dark.TLabel').pack(
            side='top', fill='x', padx=10, pady=(0, 10))
        # bind theme change
        theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: str) -> None:
        self.header.configure(image=self.icon_cache[theme])
