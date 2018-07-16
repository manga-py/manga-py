import codecs
from binascii import unhexlify, crc32
import struct
from sys import stderr

from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
from execjs import compile


class BaseLib:

    @classmethod
    def decode_escape(cls, data):  # pragma: no cover
        if isinstance(data, str):
            data = data.encode()
        try:
            data = codecs.escape_decode(data)
            return data[0]
        except Exception as e:
            print('decode_escape error %s' % e, file=stderr)
            return ''

    @classmethod
    def encode_hex(cls, data):  # pragma: no cover
        return codecs.decode(data, 'hex')

    @classmethod
    def to_sha_256(cls, data):  # pragma: no cover
        if isinstance(data, str):
            data = data.encode()
        sha = SHA256.new()
        sha.update(data)
        return sha.digest()

    @classmethod
    def decrypt_aes(cls, iv, key, data):  # pragma: no cover
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.decrypt(data)

    @classmethod
    def exec_js(cls, source, js):  # pragma: no cover
        return compile(source).eval(js)

    @classmethod
    def md5(cls, string):  # pragma: no cover
        md5 = MD5.new()
        md5.update(string.encode())
        return md5

    @classmethod
    def pack_auto(cls, int_list) -> bytes:
        """
        :param int_list: list
        :return: str
        """
        base_frm = '{}B'.format(len(int_list))
        return struct.pack(base_frm, *int_list)

    @classmethod
    def unpack_auto(cls, string) -> list:
        """
        :param string: str
        :return: tuple
        """
        if isinstance(string, str):
            string = string.encode()

        return list(string)

    @classmethod
    def str2hex(cls, string):
        hex_str = ''
        if isinstance(string, bytes):
            string = string.decode()
        for char in string:
            int_char = ord(char)
            hex_num = hex(int_char).lstrip("0x")
            hex_str += hex_num
        return hex_str

    @classmethod
    def hex2str(cls, string):
        clear_str = ''
        if isinstance(string, bytes):
            string = string.decode()
        for counter in range(0, len(string), 2):
            hex_char = string[counter] + string[counter + 1]
            clear_str += unhexlify(hex_char)
        return clear_str

    @classmethod
    def crc32(cls, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return crc32(value)
