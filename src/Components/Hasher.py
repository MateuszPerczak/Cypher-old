from threading import Thread
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from os.path import abspath, expanduser, join, exists
from os import urandom
from tkinter import ttk
from typing import Callable


class Encryptor:
    def __init__(self: object, protector: object, progress_page: ttk.Frame) -> None:
        self.files: list = []
        self.password: str = ''
        self._protector: object = protector
        self._progress_page: ttk.Frame = progress_page
        # bindings
        self.bindings: dict = {'end': [], 'start': [], 'progress': []}

    def encrypt(self: object) -> None:
        # notify event
        self.__notify('start')
        # start encryption
        _salt: bytes = self._protector.get_salt()
        _password: bytes = self._protector.encode_password(self.password)

        # generate key for encryptopn
        _key: bytes = self.__generate_key(_salt, _password)
        # remove variables
        del _salt, _password

        Thread(target=self.__worker_thread, args=(_key,), daemon=True).start()

        # notify event
        self.__notify('end')

    def __worker_thread(self: object, key: bytes) -> None:
        print(key)
        for _file in self.files:
            self.__notify('progress')
            print(_file)

    def __generate_key(self: object, salt: bytes, password: bytes) -> bytes:
        return urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend()).derive(password))

    def bind(self: object, bind_type: str, methode: Callable) -> None:
        self.bindings[bind_type].append(methode)

    def __notify(self: object, notify_type: str) -> None:
        for methode in self.bindings[notify_type]:
            methode()


class Decryptor:
    def __init__(self: object) -> None:
        pass


class Protector:
    def __init__(self: object) -> None:
        self._salt: bytes = self.__init_salt()
        self._offset: int = ord(self._salt.decode(errors='ignore')[10])

    def __init_salt(self: object) -> bytes:
        _user_folder: str = join(expanduser("~"), 'AppData', 'Local')
        _salt: bytes = b''
        if exists(join(_user_folder, 'slt.bin')):
            with open(join(_user_folder, 'slt.bin'), 'rb') as _file:
                _salt: str = _file.read()
        else:
            _salt: bytes = urandom(512)
            with open(join(_user_folder, 'slt.bin'), 'wb') as _file:
                _file.write(_salt)
        return _salt

    def get_salt(self: object) -> bytes:
        return self._salt

    def encode_password(self: object, password: str) -> bytes:
        _password: str = ''
        for index, letter in enumerate(password):
            _password += chr(ord(letter) + index + self._offset)
        return _password.encode()
