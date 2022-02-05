# 作者：我只是代码的搬运工
# coding:utf-8
import os
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app

from myapp.utils.rsa_message import RSAUtil
from myapp.utils.network import Result
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random


def users_to_json(users):
    """
    将用户转换json
    users: 用户
    """
    result = []
    for user in users:
        result.append(user.to_json())
    return result


# 重定项到首页
def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    """
    判断是否是安全的链接
    :param target:
    :return:
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


#
# def ver_password(user, i_pwd):
#     u_pwd = Coding.HexStrToBytes(user.password)
#     private_key = Coding.HexStrToBytes(user.private_key)  # 私钥转换为字节流
#     # 校验
#     flag = RSAUtil.eq(privateKey=private_key, text1=u_pwd, text2=i_pwd)
#     return flag
#
#
# def create(user, data):
#     # 生成私钥
#     user_item = user.copy()
#     private_key = RSAUtil.create_keys(user.uuid)
#     # 转字符串
#     user_item.private_key = Coding.BytesToHexStr(private_key)
#     # 加密密码
#     pwd = RSAUtil.encrypt(RSAUtil.getPublicKey(user.uuid), user.password)
#
#     user_item.password = Coding.BytesToHexStr(pwd)
#
#     user.create(user_item)
#
#     return user


# 生成随机图片
def validate_picture(length):
    # 随机颜色
    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 验证码随机数
    msg = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    width = 150
    height = 50
    # 创建一个RGB的图片
    image = Image.new('RGB', (width, height), 'white')
    # 创建字体对象
    font = ImageFont.truetype('Hiragino Sans GB.ttc', 40)
    # 画图
    draw = ImageDraw.Draw(image, 'RGB')
    code = ''
    for i in range(length):
        c = random.choice(msg)  # 随机取
        code += c
        h = random.randint(0, 4)
        draw.text([i * width / length, h], text=c, fill=rndColor(), font=font)
    # 绘制干扰线
    for n in range(10):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        begin = (x1, y1)
        end = (x2, y2)
        # 绘制直线
        draw.line([begin, end], fill=rndColor(), width=1)
    # 干扰点
    point_chance = random.randint(0, 100)
    chance = min(100, max(0, point_chance))  # 大小限制在[0, 100]
    for w in range(0, width, 10):
        for h in range(0, height, 10):
            tmp = random.randint(0, 50)
            if tmp > 200 - chance:
                draw.point((w, h), fill=(0, 0, 0))

    # 干扰圆
    for i in range(10):
        draw.point([random.randint(0, width),
                    random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 加滤镜
    image = image.filter(ImageFilter.FIND_EDGES)  # 模糊后的图片

    with open("validate.png", "wb") as f:
        image.save(f, "png")

    return image, code


def mkdir_path(path):
    """
    创建文件夹
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']
