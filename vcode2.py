# -*- coding:utf-8 -*-

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random

VERIFY_CODES = "23456789AaBbCcDdEeFfGgHhJjKkLMmNnPpQqRrSsTUuVvWwXxYyZz"
# VERIFY_CODES = "Ww"
FONTS = ['BRITANIC.TTF', 'ARLRDBD.TTF', 'trebucbd.ttf', 'msyhbd.ttc']

def randomChar():
    size = len(VERIFY_CODES)
    index = random.randint(0,size-1)
    return VERIFY_CODES[index]

def randomFont():
    size = len(FONTS)
    index = random.randint(0, size-1)
    # 创建font对象
    font = ImageFont.truetype(FONTS[index], random.randint(36, 40));
    return font


# 返回随机字母
def charRandom():
    return chr((random.randint(65, 90)))


# 返回随机数字
def numRandom():
    return random.randint(0, 9)


# 随机颜色
def colorRandom1():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机长生颜色2
def colorRandom2():
    return (random.randint(32, 115), random.randint(32, 115), random.randint(32, 115))

def get_name(num):
    result = ''
    for i in range(4):
        result = str(num % 10) + result
        num = num / 10
    return result

def generate_code(dir, num):
    width = 200
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255));

    # 创建draw对象
    draw = ImageDraw.Draw(image)

    # 填充每一个颜色
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=colorRandom1())

    # 输出文字
    loc = 0
    code = ''
    for t in range(5):
        tmp_char = randomChar()
        draw.text((loc + 10, 5), tmp_char, font=randomFont(), fill=colorRandom2())
        loc += random.randint(35, 40)
        code += tmp_char

    for i in range(0, 5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        draw.line([(x, y), (x1, y1)], colorRandom2())

    # 模糊
    # image = image.filter(ImageFilter.BLUR)

    # 旋转
    # image.rotate(random.randint(0, 60), expand=0)
    index = get_name(num)
    image.save(dir+'/%s.jpg'%index, 'jpeg')

    del draw

    return index, code

dir = 'E:/2'
mapping_file = open(dir+'/mappings.txt', 'w')
for i in range(5000):
    index, code = generate_code(dir,i)
    mapping_file.write(index + ',' + code.upper() + '\n')
    print(i)
mapping_file.close()

