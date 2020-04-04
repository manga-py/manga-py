from .base_lib import BaseLib
from loguru import logger


class KissMangaComCrypt(BaseLib):

    def decrypt(self, iv, key, data):
        iv = self.encode_hex(iv)
        key = self.to_sha_256(key)
        data = self.base64decode(data)

        try:
            return self.decrypt_aes(iv, key, data)
        except Exception as e:
            logger.error(e)
            return False
