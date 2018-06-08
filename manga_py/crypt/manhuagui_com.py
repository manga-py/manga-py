from .base_lib import BaseLib


class ManhuaGuiComCrypt(BaseLib):
    def decrypt(self, js, default=''):
        # try:
        return self.exec_js(self.js_gz_b64_data(), js)
        # except Exception:
        #     return default

    def js_gz_b64_data(self):  # FIXME
        data = """eJzNVdtymzAQ/RWHhwwqawp2mqbI60yaNr0lvaXXeJgMARFIiEQlYTt1+fcKfOt03Olj8iAQR7tn
j3YO0jiSneOzUy1zfolpxWOdC26T2djgAue4m0pxc5hF8lAkDHKc1bRZ5jhLWCxuSsmUOjIhTyPF
dneCFYsgM8l0JXmHV0WBKPYtK7CsZtIAAXfPPVu4BeOXOoN+D1aZfJW5JgMD5qm9lY9EaGbm2QhJ
hbQbMRo9qgdLMqodhzQhI+HGRviBtjUJUdcL1naJh7VtHTw9fPb86MXLV6/fHJ+8fff+w8fTT5+/
fP32/Sy6iBOWXmb51XVxw0X5QypdjSfT25+e3+vvPNp9vPfEeYgWrEpwQmpSw7m3bkEOHPS8mxIU
RFACgwJiSHEUQoY7UJkxxj4kaFkwadApmvgi0LZHoBQqb4gCDjlP2DTw51uWZrty0KfSQZ+kIxmi
bPEIPWB4EunMLcXE7kGPQIE+LbaQUVLi1DXU21N3yQvr6XCIPniIa2R7215/YBNrklEbsNViWkwg
+oV2OfT2/cAjDwooBgNTTU1yHWd2RGaxsUTH9GOTtL27kBajMLrohWTRNW3V+ZvV+bv3Q14vmHvW
supGZzrqhxiDMmPilpXK7JhQ2v4ZC/JhTpYZmy0xvkNLxHgfTZGOKscJ29ZDjFXXh6zbvbce+a/a
pWU6E/dK5Ny2LFIbf5jqmSma/eWFsakE6SgOSYLNi7JCscZP8RZiRf44wWmCylHL084j9cKBSZPf
alJOsl42Jk2aLXe7/ypb1zVd8tc2oYvrppRCC31bMleVRR7jhgtleWW5m24gW2e5Im2yNjk1/Q2+
WUKy"""
        return self.zlib_d(self.base64decode(data)).decode()
