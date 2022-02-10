from distutils import command
from tkinter import ttk, StringVar, PhotoImage
from os.path import join
from Pages.Settings import SettingsPage
from Pages.Encrypt import EncryptPage
from Pages.Progress import ProgressPage
from Pages.Decrypt import DecryptPage
from Pages.Welcome import WelcomePage


class MainPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)

        # variables
        self.theme: str = props['theme']

        self.selected_page: StringVar = StringVar(value='Encrypt')

        self.icon_cache = {
            'encrypt': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\encrypt.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\encrypt.png')
            },
            'decrypt': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\decrypt.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\decrypt.png')
            },
            'settings': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\settings.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\settings.png')
            },
        }

        # page layout
        # menu panel
        self.menu_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        # encrypt button
        self.encrypt_button: ttk.Radiobutton = ttk.Radiobutton(
            self.menu_panel, image=self.icon_cache['encrypt'][self.theme.get_theme()], variable=self.selected_page, value='encrypt', command=self.__show_page)
        self.encrypt_button.pack(side='top', anchor='c', padx=10, pady=10)
        # decrypt button
        self.decrypt_button: ttk.Radiobutton = ttk.Radiobutton(
            self.menu_panel, image=self.icon_cache['decrypt'][self.theme.get_theme()], variable=self.selected_page, value='decrypt', command=self.__show_page)
        self.decrypt_button.pack(side='top', anchor='c', padx=10, pady=(0, 10))
        # setings button
        self.settings_button: ttk.Radiobutton = ttk.Radiobutton(
            self.menu_panel, image=self.icon_cache['settings'][self.theme.get_theme()], variable=self.selected_page, value='settings', command=self.__show_page)
        self.settings_button.pack(side='bottom', anchor='c', padx=10, pady=10)

        self.menu_panel.pack(side='left', fill='both')
        # content
        self.content_panel: ttk.Frame = ttk.Frame(self)
        # settings
        self.settings_page: SettingsPage = SettingsPage(
            self.content_panel, props={'theme': props['theme']})
        self.settings_page.place(x=0, y=0, relwidth=1, relheight=1)
        # progress page
        self.progress_page: ProgressPage = ProgressPage(self.content_panel, props={
            'theme': props['theme']})
        self.progress_page.place(x=0, y=0, relwidth=1, relheight=1)
        # encrypt
        self.encrypt_page: EncryptPage = EncryptPage(
            self.content_panel, props={'theme': props['theme'], 'progress_page': self.progress_page, 'protector': props['protector']})
        self.encrypt_page.place(x=0, y=0, relwidth=1, relheight=1)

        # decrypt
        self.decrypt_page: DecryptPage = DecryptPage(
            self.content_panel, props={'theme': props['theme'], 'protector': props['protector']})
        self.decrypt_page.place(x=0, y=0, relwidth=1, relheight=1)
        # Welcome
        WelcomePage(self.content_panel).place(
            x=0, y=0, relwidth=1, relheight=1)
        # pages
        self.pages: dict = {
            'encrypt': self.encrypt_page,
            'decrypt': self.decrypt_page,
            'settings': self.settings_page,
        }

        self.content_panel.pack(side='left', fill='both', expand=True)

        # bind theme change
        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        self.encrypt_button.configure(
            image=self.icon_cache['encrypt'][self.theme.get_theme()])
        self.decrypt_button.configure(
            image=self.icon_cache['decrypt'][self.theme.get_theme()])
        self.settings_button.configure(
            image=self.icon_cache['settings'][self.theme.get_theme()])

    def __show_page(self: object) -> None:
        selected_page: str = self.selected_page.get()
        self.pages[selected_page].tkraise()
