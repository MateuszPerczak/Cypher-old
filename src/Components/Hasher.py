from threading import Thread
from tkinter.filedialog import asksaveasfile
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from os.path import expanduser, join, exists
from os import urandom, remove
from tkinter import ttk
from typing import Callable
from zipfile import ZipFile, ZIP_DEFLATED


class Encryptor:
    def __init__(self: object, protector: object, progress_page: ttk.Frame) -> None:
        self.files: list = []
        self.password: str = ''
        self._protector: object = protector
        self._progress_page: ttk.Frame = progress_page
        # bindings
        self.bindings: dict = {'end': [], 'start': []}

    def encrypt(self: object) -> None:
        # notify event
        self.__notify('start')
        # start encryption
        _salt: bytes = self._protector.get_salt()
        _password: bytes = self._protector.encode_password(self.password)
        # generate key for encryptopn
        _key: bytes = self._protector.generate_key(_salt, _password)
        # remove variables
        del _salt, _password
        # show progress page
        self._progress_page.lift()
        # start thread
        Thread(target=self.__worker_thread, args=(_key,), daemon=True).start()

    def __worker_thread(self: object, key: bytes) -> None:
        _encrypted_zip: bytes = b''
        _desktop_path: str = join(expanduser("~"), 'Desktop')
        _num_files: int = len(self.files)
        # set progress
        self._progress_page.set_max_value(_num_files + 3)
        # create zip file with all files
        with ZipFile('encrypted.zip', 'w', compression=ZIP_DEFLATED, compresslevel=9) as zip_file:
            for index, _file in enumerate(self.files):
                zip_file.write(_file, _file.split('/')[-1])
                self._progress_page.set_progress(index)
        # encrypt zip file
        with open('encrypted.zip', 'rb') as zip_file:
            _encrypted_zip = Fernet(key).encrypt(zip_file.read())
        self._progress_page.set_progress(_num_files + 1)
        # ask user where to place decrypted file
        _file: object = asksaveasfile(mode='wb', defaultextension='.zip', filetypes=[
                                      ('Zip archive', '.zip')], initialfile="encrypted")
        if _file:
            _file.write(_encrypted_zip)
            _file.close()
        self._progress_page.set_progress(_num_files + 2)
        # delete old zip file
        remove('encrypted.zip')
        self._progress_page.set_progress(_num_files + 3)
        # notify event
        self.__notify('end')

    def bind(self: object, bind_type: str, methode: Callable) -> None:
        self.bindings[bind_type].append(methode)

    def __notify(self: object, notify_type: str) -> None:
        for methode in self.bindings[notify_type]:
            methode()


class Decryptor:
    def __init__(self: object, protector: object) -> None:
        self.file: str = ''
        self.password: str = ''
        self._protector: object = protector
        # bindings
        self.bindings: dict = {'end': [],
                               'start': [], 'success': [], 'error': []}

    def decrypt(self: object) -> None:
        # notify event
        self.__notify('start')
        # start encryption
        _salt: bytes = self._protector.get_salt()
        _password: bytes = self._protector.encode_password(self.password)

        # generate key for encryptopn
        _key: bytes = self._protector.generate_key(_salt, _password)
        # remove variables
        del _salt, _password
        # start thread
        Thread(target=self.__worker_thread, args=(_key,), daemon=True).start()

    def __worker_thread(self: object, key: bytes) -> None:
        _encrypted_zip: bytes = b''

        with open(self.file, 'rb') as encrypted_zip:
            _encrypted_zip = encrypted_zip.read()
        # decrypt zip file
        try:
            _decrypted_zip: bytes = Fernet(key).decrypt(_encrypted_zip)
        except Exception as _:
            self.__notify('error')
            self.__notify('end')
            return None
        # ask user where to place decrypted file
        _file: object = asksaveasfile(mode='wb', defaultextension='.zip', filetypes=[
                                      ('Zip archive', '.zip')], initialfile="decrypted")
        if _file:
            _file.write(_decrypted_zip)
            _file.close()
            self.__notify('success')

        # notify event
        self.__notify('end')

    def bind(self: object, bind_type: str, methode: Callable) -> None:
        self.bindings[bind_type].append(methode)

    def __notify(self: object, notify_type: str) -> None:
        for methode in self.bindings[notify_type]:
            methode()


class Protector:
    def __init__(self: object) -> None:
        self._salt: bytes = self.__init_salt()
        self._offset: int = ord(self._salt.decode(errors='ignore')[10])
        # public key
        self._public_key: bytes = b'WmgfNWRns0ClyhhdD55T1LO1iD4KLMmiI4ZOI-eZLY0='

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

    def generate_key(self: object, salt: bytes, password: bytes) -> bytes:
        return urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend()).derive(password))

    def export_identity(self: object) -> bytes:
        return self._encrypt_salt(self._salt)

    def import_identity(self: object, identity_file: str) -> None:
        _user_folder: str = join(expanduser("~"), 'AppData', 'Local')
        with open(join(_user_folder, 'slt.bin'), 'wb') as _file:
            with open(identity_file, 'rb') as _idt_file:
                _file.write(self._decrypt_salt(_idt_file.read()))
                self.__init_salt()

    def _encrypt_salt(self: object, salt: bytes) -> bytes:
        return Fernet(self._public_key).encrypt(salt)

    def _decrypt_salt(self: object, salt: bytes) -> bytes:
        return Fernet(self._public_key).decrypt(salt)
