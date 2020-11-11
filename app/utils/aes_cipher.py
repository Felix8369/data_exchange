import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key=None, iv=None):
        _key = 'cD19HMyRXaj0674AR8hYmwYOyypuX7y7'
        _iv = base64.b64decode('S3A5nfu2JJ+fwc6i4zIAaQ==')

        self.key = key or _key
        self.iv = iv or _iv

    def __pad(self, s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def __unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        return base64.b64encode(cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        return self.__unpad(cipher.decrypt(enc)).decode('utf-8')
