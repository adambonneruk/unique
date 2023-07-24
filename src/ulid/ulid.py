import os
import time
import codecs

ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
LENCODING = len(ENCODING)

class Ulid:
    """ulid is a universally unique lexicographically sortable identifier"""
    def __init__(self):
        self._ulid = self.__generate_ulid()

    # Private Methods
    def __generate_ulid(self):
        return self.__encode_time_10bytes(int(time.time()*1000)) + self.__encode_random_16bytes()

    def __encode_time_10bytes(self, x):
        s = ''
        while len(s) < 10:
            x, i = divmod(x, LENCODING)
            s = ENCODING[i] + s
        return s

    def __encode_random_16bytes(self):
        b = os.urandom(10)
        x = int(codecs.encode(b, 'hex'), 16)
        s = ''
        while len(s) < 16:
            x, i = divmod(x, LENCODING)
            s = ENCODING[i] + s
        return s

    # Public Methods
    def __str__(self):
        return str(self._ulid)
