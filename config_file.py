import hashlib
from os.path import exists, basename
from typing import Final


class ConfigFile:
    def __init__(self, file_name: str) -> object:
        self._file_name: Final = file_name
        self._exists: Final = exists(self._file_name)
        self._md5: Final = ConfigFile._md5(self._file_name) if self._exists else f'File "{file_name}" not found.'

    @property
    def file_name(self):
        return self._file_name

    @property
    def md5(self):
        if not self.exists:
            return None

        return self._md5

    @property
    def exists(self):
        return self._exists

    @property
    def base_name(self):
        return basename(self._file_name)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.md5 == other.md5

        return False

    @staticmethod
    def _md5(file_name):
        hash_md5 = hashlib.md5()
        with open(file_name, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
