"""
original ulid code taken from Massimo Di Pierro, https://github.com/mdipierro/ulid
adapted into a clean class for use within a python module by Adam Bonner, adambonneruk

---

The MIT License (MIT)

Copyright (c) 2016 Massimo Di Pierro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
