
from .base_lib import BaseLib


class KissMangaComCrypt(BaseLib):

    def decrypt(self, iv, key, data):
        iv = self.encode_hex(iv)
        key = self.to_sha_256(key)
        data = self.base64decode(data)

        try:
            return self.decrypt_aes(iv, key, data).decode('utf-8').strip()
        except Exception:
            return False
