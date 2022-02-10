from tkinter import ttk, PhotoImage, Canvas, Event
from Components.File import FilePanel
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
from Components.Hasher import Encryptor


class EncryptPage(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        # variables
        self.theme: str = props['theme']
        root: object = self._nametowidget('.')
        self.is_password_visible: bool = False
        self.files: list = []
        # encryptor object
        self.encryptor: Encryptor = Encryptor(
            protector=props['protector'], progress_page=props['progress_page'])

        # bind events
        self.encryptor.bind('start', self.__freeze_page)
        self.encryptor.bind('end', self.__restore_page)
        # icons
        self.icon_cache = {
            'add': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\add.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\add.png')
            },
            'remove': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\remove.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\remove.png')
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
            'file': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\file.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\file.png')
            },
            'delete': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\delete.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\delete.png')
            },
        }
        # content
        scrollbar: ttk.Scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side='right', fill='y')

        left_frame: ttk.Frame = ttk.Frame(self)

        ttk.Label(left_frame, text='Encrypt').pack(
            side='top', fill='x', padx=10, pady=(10, 5))
        action_panel: ttk.Frame = ttk.Frame(left_frame)
        # add button
        self.add_button: ttk.Button = ttk.Button(
            action_panel, image=self.icon_cache['add'][self.theme.get_theme()], command=self.__add_files)
        self.add_button.pack(side='left', padx=(10, 0))
        # remove button
        self.remove_button: ttk.Button = ttk.Button(
            action_panel, image=self.icon_cache['remove'][self.theme.get_theme()], command=self.__remove_all)
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
        # encrypt button
        self.encrypt_button: ttk.Button = ttk.Button(
            action_panel, image=self.icon_cache['start'][self.theme.get_theme()], command=self.__encrypt)
        self.encrypt_button.pack(side='right', padx=(0, 10))
        action_panel.pack(side='top', fill='x')
        # scrollable frame
        self.canvas: Canvas = Canvas(
            left_frame, bg=root['background'], bd=0, highlightthickness=0, yscrollcommand=scrollbar.set, takefocus=False)
        # link scrollbar to canvas
        scrollbar.configure(command=self.canvas.yview)
        # create content frame
        self.content: ttk.Frame = ttk.Frame(self.canvas)
        self.content.bind('<Expose>', lambda _: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        # create window insode a canvas
        self.content_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor='nw')
        self.canvas.bind('<Expose>', lambda _: self.canvas.itemconfigure(
            self.content_window, width=self.canvas.winfo_width(), height=0))
        # pack everything
        self.canvas.pack(side='top', fill='both', expand=True, pady=10)
        # bind mouse scroll to move canvas
        root.bind('<MouseWheel>', self.__on_wheel)
        left_frame.pack(side='left', fill='both', expand=True)
        # apple theme change
        self.theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: object) -> None:
        self.add_button.configure(image=self.icon_cache['add'][theme])
        self.remove_button.configure(image=self.icon_cache['remove'][theme])
        self.password_image.configure(image=self.icon_cache['key'][theme])
        self.encrypt_button.configure(image=self.icon_cache['start'][theme])
        self.show_button.configure(image=self.icon_cache['show'][theme])
        # update canvas background
        '''change l8er'''
        self.canvas.configure(bg=self._nametowidget('.')['background'])

    def __show_password(self: object) -> None:
        if self.is_password_visible:
            self.is_password_visible = False
            self.password_entry.configure(show='-')
        else:
            self.is_password_visible = True
            self.password_entry.configure(show='')

    def __on_wheel(self: object, event: Event) -> None:
        self.canvas.yview_scroll(
            int(-1.6*(event.delta/120)), 'units')

    def __add_files(self: object) -> None:
        _files: tuple = askopenfilenames(
            filetypes=[('All Files', '*.*')], title='Select files to encrypt.')
        if _files:
            for file in _files:
                if file in self.files:
                    continue
                self.files.append(file)
                FilePanel(self.content, props={
                          'theme': self.theme, 'file': file, 'icon_cache': self.icon_cache, 'files': self.files}).pack(side='top', fill='x', padx=10, pady=(10, 0))

    def __remove_all(self: object) -> None:
        for panel in self.content.winfo_children():
            panel.remove_self()
        # move canvas to top
        self.canvas.yview_moveto(0)
        self.content.configure(height=1)

    def __verify(self: object) -> bool:
        password: str = self.password_entry.get()
        if not self.files:
            messagebox.showerror('Cypher', 'No files to encrypt.')
            return False
        if not password:
            messagebox.showerror('Cypher', 'Password is required.')
            return False
        return True

    def __encrypt(self: object) -> None:
        if self.__verify():
            self.encryptor.files = self.files.copy()
            self.encryptor.password = self.password_entry.get()
            self.encryptor.encrypt()

    def __freeze_page(self: object) -> None:
        widgets: tuple = (self.add_button, self.remove_button,
                          self.encrypt_button, self.show_button, self.password_entry)
        # disable widgets
        for widget in widgets:
            widget.state(["disabled"])

    def __restore_page(self: object) -> None:
        widgets: tuple = (self.add_button, self.remove_button,
                          self.encrypt_button, self.show_button, self.password_entry)
        # enable widgets
        for widget in widgets:
            widget.state(["!disabled"])

        # delete all data
        self.__remove_all()
        self.password_entry.delete(0, 'end')
