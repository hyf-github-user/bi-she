import rsa
from settings import RAS_PATH


class RSAUtil:
    @staticmethod
    def create_keys(name):
        """
        生成公钥和私钥，公钥保存在`RAS_PATH`+name.pem
        :param name:
        :return:
        """

        (pubkey, privkey) = rsa.newkeys(1024)
        # 保存公钥
        pub = pubkey.save_pkcs1()
        path = f'{RAS_PATH}{name}.pem'
        with open(path, 'wb+') as f:
            f.write(pub)
        # 获取私钥
        pri = privkey.save_pkcs1()
        return pri

    @staticmethod
    def encrypt(public_key, text):
        """
        使用公钥加密
        :return:
        """
        pubkey = rsa.PublicKey.load_pkcs1(public_key)
        original_text = text.encode('utf8')
        crypt_text = rsa.encrypt(original_text, pubkey)
        return crypt_text

    @staticmethod
    def decrypt(crypt_text, private_key):
        """
        使用私钥解密
        :param crypt_text:加密后的文本
        :param private_key:私钥的位置和名称
        :return:
        """
        privateKey = rsa.PrivateKey.load_pkcs1(private_key)
        lase_text = rsa.decrypt(crypt_text, privateKey).decode()
        return lase_text

    @staticmethod
    def getPublicKey(name):
        """
        根据名称读取公钥
        :param name:
        :return:
        """
        with open(f'{RAS_PATH}{name}.pem', 'rb') as f:
            p = f.read()
        return p

    @staticmethod
    def eq(privateKey, text1, text2):
        """
        使用私钥解密text1，对比text2是否相等
        :param privateKey:
        :param text1:
        :param text2:
        :return:
        """
        result = RSAUtil.decrypt(text1, privateKey)
        return str(result) == str(text2)


def HexStrToBytes(text):
    return bytes.fromhex(text)


def BytesToHexStr(text):
    """
    字节转hex字符串
    :param text:
    :return:
    """
    return text.hex()


if __name__ == '__main__':
    uuid = "5574f9a67e4b4713a743b5d609294149"
    private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIICYAIBAAKBgQDFjAjAumTzcQV2MvHf9MmgaHXSRsIrwjLtL+b0FNQNXzf9abuG\n1IxxoMc3tCLzdB42SgVx8k/RbKTrcbubEAbJ/8lRZv+WbTSlweUQRzqDZfhMtaTS\nZHgkd+UKo/FoJCdSl4+2aA4z4AlDkwlNuNCqG52R+A0jHnixWA2/xiK4nQIDAQAB\nAoGBAKIqVVkY6hwpsIkaQxJM2WNzvRyz91uCnNm2lAnUO0sK2mSN8mI5g10X1dI1\nbueZb9+zHgsvFjTd0fhxMQsYUFwFiOKK4SnCTfvm/hJNlebxaXpIcX+kkECI6FSI\nYAfWUaKvv+brp0p4J07pwgpwYuoDehiSIWEoFHzf0MoPsY3lAkUA5Z3IjnFgOO/Y\nJUxwcdU46d9cmnBbTPQUF12LsZibvP685zY0V/WM59OlAGlCXizjsELENNY8EjGU\nO3C2HlPuCMxO368CPQDcPuyRQgJ3X2PMIUFT6SFKzMkJIxAL/kkGw63tOd241C/z\nES1dVZHYEgWr3n4pty5/PyRFYS3see/Z03MCRFu8MO8vvpigwgMMyfPAkw9kzHNr\nJh7VeN1o4zGd3cKhJ0lcb4cgtB2+gbJrWzeSyZiW5BqT6MYABs/ElQ4CzBu5vF1D\nAjxEBOrqsYgxdbRMhri2QXmWsEgmGj4Kdi33eNduPEDNpDpqxxNLj/HK2UYHHl+4\nYmppwgZhpvGX5tC8ZSECRHxbTo/zpqqkqz7Ou9qYR8GtQO7Wfm1StdEm6bEdlWRV\nCmcIEyrY1FVYBRz3O7HucMWdqrJmtV4ZdH7YpCofliIR8gUq\n-----END RSA PRIVATE KEY-----\n'
    pwd = b'\x85y\x83\x18\xa3\x19;\xcd\x08\x8a\xe7\xca\xc3\x10O\xbe\xfa_,\n(\x0b\x9d\x85\xcbwmi\xbe\xaf\xa9\x85\xef\xc7.\x19\xc7\x8f\x9fN\xfa\xa6\xf6g\xc7D\xef{.\xd9{\x86+\xc2Cd\x1d\x83@7\x9d>U\xbd\x11\x99O\xc1YB\tw\xdaV=f)\rm\xfb\x92U\xfe\x80f\xda\xe5\x9b\xe8!Ahe\x92\xdbT\x07(\x1a\xb6\xa0/\xbb;\xc839\xcb@\xea\xb4\x85\x1d*\x87\xb4t\xc9\xc2\xfe9\x16\xe8Pb<v\x8d'
    rp = RSAUtil.encrypt(RSAUtil.getPublicKey(uuid), '123456')
    print(rp)
    res = RSAUtil.eq(privateKey=private_key, text1=pwd, text2=123456)
    print(res)
