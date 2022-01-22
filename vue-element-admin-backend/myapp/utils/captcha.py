# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :captcha.py
# 时间    :2022/1/22 17:50
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont


class Captcha:

    def __init__(self, length=4, width=150, height=50):
        self.msg = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.length = length
        self.width = width
        self.height = height
        self.code = ''
        # 创建一个RGB的图片
        self.image = Image.new('RGB', (self.width, self.height), 'white')
        # 创建字体对象
        self.font = ImageFont.truetype('Hiragino Sans GB.ttc', 40)
        # 画图
        self.draw = ImageDraw.Draw(self.image, 'RGB')

    # 随机颜色
    def randColor(self):
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    def generate_captcha(self):
        for i in range(self.length):
            c = random.choice(self.msg)  # 随机取
            self.code += c
            h = random.randint(0, 4)
            self.draw.text([i * self.width / self.length, h], text=c, fill=self.randColor(), font=self.font)
        # 绘制干扰线
        for n in range(10):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            begin = (x1, y1)
            end = (x2, y2)
            # 绘制直线
            self.draw.line([begin, end], fill=self.randColor(), width=1)
        # 干扰点
        point_chance = random.randint(0, 100)
        chance = min(100, max(0, point_chance))  # 大小限制在[0, 100]
        for w in range(0, self.width, 10):
            for h in range(0, self.height, 10):
                tmp = random.randint(0, 50)
                if tmp > 200 - chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

        # 干扰圆
        for i in range(10):
            self.draw.point([random.randint(0, self.width),
                             random.randint(0, self.height)], fill=self.randColor())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.randColor())

        # 加滤镜
        self.image = self.image.filter(ImageFilter.FIND_EDGES)  # 模糊后的图片

        return self.image, self.code

    def save_captcha(self):
        """
        保存生成的验证码
        :return:
        """
        with open("validate.png", "wb") as f:
            self.image.save(f, "png")


# c = Captcha()
# image, code = c.generate_captcha()
# print(image, code)
