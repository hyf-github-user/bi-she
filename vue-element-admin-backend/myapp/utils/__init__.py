# 作者：我只是代码的搬运工
# coding:utf-8
from myapp.utils import Coding
from myapp.utils.rsa_message import RSAUtil


def users_to_json(users):
    result = []
    for user in users:
        result.append(user.to_json())
    return result


def ver_password(user, i_pwd):
    u_pwd = Coding.HexStrToBytes(user.password)
    private_key = Coding.HexStrToBytes(user.private_key)  # 私钥转换为字节流
    # 校验
    flag = RSAUtil.eq(privateKey=private_key, text1=u_pwd, text2=i_pwd)
    return flag


def create(user, data):
    # 生成私钥
    user_item = user.copy()
    private_key = RSAUtil.create_keys(user.uuid)
    # 转字符串
    user_item.private_key = Coding.BytesToHexStr(private_key)
    # 加密密码
    pwd = RSAUtil.encrypt(RSAUtil.getPublicKey(user.uuid), user.password)

    user_item.password = Coding.BytesToHexStr(pwd)

    user.create(user_item)

    return user
