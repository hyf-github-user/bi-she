
# 生成随机图片
def validate_picture(length):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    import random

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


image, code = validate_picture(4)
print("验证码是: ", code)
