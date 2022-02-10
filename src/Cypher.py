try:
    from tkinter import Tk
    from Components import View
    from Components.Hasher import Protector
    from Components.Debugger import Debugger
    from Pages.Init import InitPage
    from Pages.Main import MainPage
    from os.path import join
except Exception as err:
    exit(err)


class Cypher(Tk):
    def __init__(self: Tk) -> Tk:
        super().__init__()
        # window properties
        self.withdraw()
        self.title('Cypher')
        self.iconbitmap(join('Resources', 'Icons', 'Static', 'icon.ico'))
        self.geometry(
            f'735x432+{int(self.winfo_x() + ((self.winfo_screenwidth() / 2) - 367))}+{int(self.winfo_y() + ((self.winfo_screenheight() / 2) - 216))}')
        self.minsize(735, 432)
        # apply custom layout
        View.Layout(self)
        # init theme
        self.theme: object = View.Theme(self)
        self.theme.apply('System')

        # protector instance
        self._protector: Protector = Protector()
        # debugger instance
        self.bind('<F12>', lambda _: Debugger(self))

        self.init_page: InitPage = InitPage(self)
        self.init_page.place(x=0, y=0, relwidth=1, relheight=1)
        self.deiconify()
        # init ui after initialization
        self.after(1000, self.__init_ui)
        self.mainloop()

    def __init_ui(self: Tk) -> None:
        # load main page
        self.main_page: MainPage = MainPage(
            self, props={'theme': self.theme, 'protector': self._protector})
        self.main_page.place(x=0, y=0, relwidth=1, relheight=1)
        del self.init_page


if __name__ == '__main__':
    Cypher()
