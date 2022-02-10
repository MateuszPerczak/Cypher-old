from tkinter import Tk, ttk
from typing import Callable
from Components.SystemTheme import get_theme


class Layout:
    def __init__(self: object, parent: Tk) -> object:
        # pass parent object
        self.parent = parent
        # init theme object
        self.parent.layout = ttk.Style()
        # set theme to clam
        self.parent.layout.theme_use('clam')
        # button
        self.parent.layout.layout('TButton', [('Button.padding', {
                                  'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})])
        # radiobutton
        self.parent.layout.layout('TRadiobutton', [('Radiobutton.padding', {
                                  'sticky': 'nswe', 'children': [('Radiobutton.label', {'sticky': 'nswe'})]})])
        # scrollbar
        self.parent.layout.layout('Vertical.TScrollbar', [('Vertical.Scrollbar.trough', {'children': [
                                  ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        # entry
        self.parent.layout.layout('TEntry', [('Entry.padding', {
                                  'sticky': 'nswe', 'children': [('Entry.textarea', {'sticky': 'nswe'})]})])


class Theme:
    def __init__(self: object, parent: Tk) -> None:
        # pass parent object
        self.parent = parent
        self.colors: dict = {'Dark': ['#111', '#212121', '#333', '#fff'], 'Light': [
            '#fff', '#ecf0f1', '#ecf0f1', '#000']}
        # get system theme
        self.system_theme: str = get_theme()
        self.colors['System'] = self.colors[self.system_theme]
        # set default applied theme
        self.applied_theme: str = 'Light'
        # bindings
        self.bindings: dict = {'changed': []}

    def apply(self: object, theme: str) -> None:
        self.applied_theme = theme
        # pass parent object
        self.parent.configure(background=self.colors[theme][1])
        # frames
        self.parent.layout.configure(
            'TFrame', background=self.colors[theme][1])
        self.parent.layout.configure(
            'dark.TFrame', background=self.colors[theme][0])
        # radiobutton
        self.parent.layout.configure('TRadiobutton', background=self.colors[theme][0], relief='flat', font=(
            'catamaran 13 bold'), foreground=self.colors[theme][3], anchor='w', padding=5, width=12)
        self.parent.layout.map('TRadiobutton', background=[('pressed', '!disabled', self.colors[theme][1]), (
            'active', self.colors[theme][1]), ('selected', self.colors[theme][1])])
        self.parent.layout.configure('small.TRadiobutton',
                                     anchor='center', padding=5, width=8)
        # label
        self.parent.layout.configure('TLabel', background=self.colors[theme][1], relief='flat', font=(
            'catamaran 13 bold'), foreground=self.colors[theme][3])
        self.parent.layout.configure(
            'dark.TLabel', background=self.colors[theme][0])
        self.parent.layout.configure(
            'big.TLabel', font=('catamaran 18 bold'))
        self.parent.layout.configure(
            'small.dark.TLabel', font=('catamaran 9 bold'))
        self.parent.layout.configure(
            'small.TLabel', font=('catamaran 9 bold'), background=self.colors[theme][1])
        # button
        self.parent.layout.configure('TButton', background=self.colors[theme][0], relief='flat', font=(
            'catamaran 13 bold'), foreground=self.colors[theme][3], anchor='w', width=10)
        self.parent.layout.map('TButton', background=[('pressed', '!disabled', self.colors[theme][1]), (
            'active', self.colors[theme][1]), ('selected', self.colors[theme][1])])
        self.parent.layout.configure('center.TButton', anchor='c')
        # entry
        self.parent.layout.configure('TEntry', background=self.colors[theme][0], insertcolor=self.colors[theme][3], foreground=self.colors[theme]
                                     [3], fieldbackground=self.colors[theme][0], selectforeground=self.colors[theme][3], selectbackground=self.colors[theme][2])
        self.parent.layout.map('TEntry', foreground=[
            ('active', '!disabled', 'disabled', self.colors[theme][3])])
        # scrollbar
        self.parent.layout.configure('Vertical.TScrollbar', gripcount=0, relief='flat', background=self.colors[theme][1], darkcolor=self.colors[
                                     theme][1], lightcolor=self.colors[theme][1], troughcolor=self.colors[theme][1], bordercolor=self.colors[theme][1])
        self.parent.layout.map('Vertical.TScrollbar', background=[('pressed', '!disabled', self.colors[theme][0]), (
            'disabled', self.colors[theme][1]), ('active', self.colors[theme][0]), ('!active', self.colors[theme][0])])

        # progressbar
        self.parent.layout.configure('Horizontal.TProgressbar', background=self.colors[theme][1], lightcolor=self.colors[theme][0],
                                     darkcolor=self.colors[theme][0], bordercolor=self.colors[theme][0], troughcolor=self.colors[theme][0], thickness=2)
        # notify event
        self.__notify('changed')

    def get_theme(self: object) -> str:
        if self.applied_theme == 'System':
            return self.system_theme
        return self.applied_theme

    def get_internal_theme(self: object) -> str:
        return self.applied_theme

    def theme_changed(self: object, theme: str) -> None:
        for methode in self.__binded_methods:
            methode(theme)

    def get_colors(self: object, theme: str) -> list:
        return self.colors[theme]

    def bind(self: object, bind_type: str, methode: Callable) -> None:
        self.bindings[bind_type].append(methode)

    def unbind(self: object, methode: Callable) -> None:
        for key in self.bindings:
            if methode in self.bindings[key]:
                self.bindings[key].remove(methode)

    def __notify(self: object, notify_type: str) -> None:
        for methode in self.bindings[notify_type]:
            methode()
