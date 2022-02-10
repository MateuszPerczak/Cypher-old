from tkinter import ttk, PhotoImage
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from Components.File import DecryptionFile
from Components.Hasher import Decryptor


class DecryptPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)

        self.theme: str = props['theme']
        self.is_password_visible: bool = False
        self.file_path: str = ''
        self.decryptor: Decryptor = Decryptor(protector=props['protector'])
        # bind events
        self.decryptor.bind('success', self.__success)
        self.decryptor.bind('error', self.__error)

        self.icon_cache = {
            'plus': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\plus.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\plus.png')
            },
            'key': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\key.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\key.png')
            },
            'start': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\start.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\start.png')
            },
            'show': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\show.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\show.png')
            },
            'encrypt': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\encrypt.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\encrypt.png')
            },
            'decrypt': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\decrypt.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\decrypt.png')
            },
            'close': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\close.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\close.png')
            },
            'file': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\file.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\file.png')
            },
        }

        # content
        ttk.Label(self, text='Decrypt').pack(
            side='top', fill='x', padx=10, pady=(10, 5))

        # content
        action_panel: ttk.Frame = ttk.Frame(self)

        self.add_button: ttk.Button = ttk.Button(
            action_panel, image=self.icon_cache['plus'][self.theme.get_theme()], command=self.__add_files)
        self.add_button.pack(side='left', padx=(10, 0))
        # remove button
        self.remove_button: ttk.Button = ttk.Button(
            action_panel, image=self.icon_cache['close'][self.theme.get_theme()], command=self.__remove_all)
        self.remove_button.pack(side='left', padx=(10, 0))
        # password entry
        password_panel: ttk.Frame = ttk.Frame(
            action_panel, style='dark.TFrame')
        self.password_image: ttk.Label = ttk.Label(
            password_panel, image=self.icon_cache['key'][self.theme.get_theme()], style='dark.TLabel', padding=3)
        self.password_image.pack(side='left')
        self.password_entry: ttk.Entry = ttk.Entry(
            password_panel, font=('catamaran 13 bold'), show='-')
        self.password_entry.pack(side='left', padx=5)
        self.show_button: ttk.Button = ttk.Button(
            password_panel, image=self.icon_cache['show'][self.theme.get_theme()], command=self.__show_password)
        self.show_button.pack(side='left', padx=(0, 5))
        password_panel.pack(side='left', padx=(10, 0))
        # decrypt button
        self.decrypt_button: ttk.Button = ttk.Button(
            action_panel, image=self.icon_cache['start'][self.theme.get_theme()], command=self.__decrypt)
        self.decrypt_button.pack(side='right', padx=(0, 24))
        action_panel.pack(side='top', fill='x')
        self.file_panel: ttk.Frame = ttk.Frame(self)

        self.file_panel.pack(side='top', fill='both',
                             expand=True, padx=(0, 14), pady=(10, 0))

        # apple theme change
        self.theme.bind('changed', self.__on_theme_changed)

    def __on_theme_changed(self: object) -> None:
        self.add_button.configure(
            image=self.icon_cache['plus'][self.theme.get_theme()])
        self.password_image.configure(
            image=self.icon_cache['key'][self.theme.get_theme()])
        self.decrypt_button.configure(
            image=self.icon_cache['start'][self.theme.get_theme()])
        self.show_button.configure(
            image=self.icon_cache['show'][self.theme.get_theme()])
        self.remove_button.configure(
            image=self.icon_cache['close'][self.theme.get_theme()])

    def __show_password(self: object) -> None:
        if self.is_password_visible:
            self.is_password_visible = False
            self.password_entry.configure(show='-')
        else:
            self.is_password_visible = True
            self.password_entry.configure(show='')

    def __add_files(self: object) -> None:
        # remove all files
        self.__remove_all()
        _file_path = askopenfilename(title='Choose a encrypted file', filetypes=[
            ('All Files', '*.*')])
        self.file_path = _file_path
        if _file_path:
            DecryptionFile(self.file_panel, props={
                'theme': self.theme, 'icon_cache': self.icon_cache, 'file': self.file_path}).pack(side='top', fill='x', padx=10)

    def __remove_all(self: object) -> None:
        for panel in self.file_panel.winfo_children():
            panel.remove_self()
            panel.destroy()
        self.password_entry.delete(0, 'end')

    def __verify(self: object) -> bool:
        password: str = self.password_entry.get()
        if not self.file_path:
            messagebox.showerror('Cypher', 'No files to encrypt.')
            return False
        if not password:
            messagebox.showerror('Cypher', 'Password is required.')
            return False
        return True

    def __decrypt(self: object) -> None:
        if self.__verify():
            self.decryptor.file = self.file_path
            self.decryptor.password = self.password_entry.get()
            self.decryptor.decrypt()

    def __success(self: object) -> None:
        for panel in self.file_panel.winfo_children():
            panel.set_decrypt()
        self.password_entry.delete(0, 'end')

    def __error(self: object) -> None:
        messagebox.showerror('Cypher', 'Decryption failed')
