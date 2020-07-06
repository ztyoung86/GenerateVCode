# -*- coding: utf-8 -*-
import random
import os

from PIL import Image, ImageDraw, ImageFont


chars_file = open('chars.txt')
uni_chars = chars_file.readlines()

class RandomChar():
    """用于随机生成汉字"""

    @staticmethod
    def Unicode():
        # val = random.randint(0x4E00, 0x9FBF)
        index = random.randint(0,len(uni_chars)-1)
        char = uni_chars[index].replace('\u','0x')
        val = int(char,16)
        return unichr(val)

    @staticmethod
    def GB2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = (head << 8) | (body << 4) | tail
        str = "%x" % val
        return str.decode('hex').decode('gb2312')


class ImageChar():
    def __init__(self, fontColor=(0, 0, 0), size=(150, 45), fontPath='msyhbd.ttc', bgColor=(255, 255, 255), fontSize=21):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bgColor)
        self.mapping = ''
        self.chars = []
        self.single_chars = []
        self.single_images = []
        self.single_image_char = {}

    def rotate(self):
        self.image.rotate(random.randint(0, 30), expand=0)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw

    def randRGB(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 随机颜色
    def colorRandom1(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机长生颜色2
    def colorRandom2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB())
        del draw

    def drawPoints(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.point(self.randPoint(), self.randRGB())
        del draw

    def randChinese(self, num):
        gap = 10
        start = 5
        for i in range(0, num):
            char = RandomChar().Unicode()
            while char in self.chars:
                char = RandomChar().Unicode()
            self.single_chars.append(char)
            self.chars.append(char)
            x = start + 25 * i + random.randint(0, gap) + gap * i
            y = random.randint(0, 12)
            text_image = Image.new('RGB', (50,50), self.bgColor)
            draw = ImageDraw.Draw(text_image)
            draw.text((10,10), char, font=self.font, fill=self.colorRandom2())
            del draw
            text_image = text_image.rotate(random.randint(-30, 30), expand=0)
            text_image = text_image.crop((8,8,43,43))
            box = (x, y, x + 35, y + 35)
            self.image.paste(text_image,box)
        self.drawPoints(200)
        self.randLine(5)

    def create_single_images(self):
        for char in self.single_chars:
            single_image = Image.new('RGB', (45, 45), self.bgColor)
            text_image = Image.new('RGB', (50, 50), self.bgColor)
            draw = ImageDraw.Draw(text_image)
            draw.text((10, 10), char, font=self.font, fill=self.colorRandom2())
            del draw
            text_image = text_image.rotate(random.randint(-30, 30), expand=0)
            text_image = text_image.crop((8, 8, 43, 43))
            box = (5, 5, 5 + 35, 5 + 35)
            single_image.paste(text_image, box)
            draw = ImageDraw.Draw(single_image)
            # 划线
            for i in range(0, 3):
                draw.line([(random.randint(0, 45), random.randint(0, 45)),(random.randint(0, 45), random.randint(0, 45))], self.randRGB())
            # 画点
            for i in range(0, 80):
                draw.point((random.randint(0, 45), random.randint(0, 45)), self.randRGB())
            del draw
            self.single_images.append(single_image)
            self.single_image_char[single_image] = char

    def save(self, path):
        self.image.save(path)

    def save_single(self,dir):
        random.shuffle(self.single_images)
        tmp_mapping = {}
        i = 0
        for image in self.single_images:
            char = self.single_image_char[image]
            if char in self.chars:
                tmp_mapping[char] = i
            image.save(dir+'/'+str(i)+'.jpg')
            i += 1
        for char in self.chars:
            index = tmp_mapping[char]
            self.mapping += str(index)

def get_name(num):
    result = ''
    for i in range(4):
        result = str(num % 10) + result
        num = num / 10
    return result


selected_num = 9
dir = 'E:/5_new'
mapping_file = open(dir+'/mappings.txt', 'w')

for n in range(5000):
    char_code = ImageChar()
    char_code.randChinese(4)

    for i in range(selected_num - len(char_code.single_chars)):
        char = RandomChar().Unicode()
        while char in char_code.single_chars:
            char = RandomChar().Unicode()
        char_code.single_chars.append(char)
    char_code.create_single_images()
    index = get_name(n)
    os.makedirs(dir+'/'+index)
    char_code.save(dir+'/'+index + '/%s.jpg' % index)
    char_code.save_single(dir+'/'+index)
    mapping_file.write(index+','+char_code.mapping+'\n')
    print n
mapping_file.close()