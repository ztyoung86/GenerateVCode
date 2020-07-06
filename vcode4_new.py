# -*- coding: utf-8 -*-
import random

from PIL import Image, ImageDraw, ImageFont

chars_file = open('chars.txt')
uni_chars = chars_file.readlines()

spec_chars = [u'回', u'日', u'口', u'田', u'一', u'三', u'二', u'米', u'十', u'曰']

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
        self.content = ''
        self.rotate_index = 0
        self.chars = []

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
        self.rotate_index = random.randint(0, num-1)
        gap = 12
        start = 5
        self.content = ''
        self.drawPoints(250)
        for i in range(0, num):
            char = RandomChar().Unicode()
            while char in spec_chars or char in self.chars:
                char = RandomChar().Unicode()
            self.chars.append(char)
            x = start + self.fontSize * i + random.randint(5, gap) + gap * i
            y = random.randint(0, 15)
            self.drawText((x, y), char, self.colorRandom2())
            if i == self.rotate_index:
                box = (x,y,x+25,y+25)
                rotate_image = self.image.crop(box)
                rotate_image = rotate_image.rotate(90)
                self.image.paste(rotate_image,box)
        self.drawPoints(50)
        self.randLine(5)

    def save(self, path):
        self.image.save(path)

def get_name(num):
    result = ''
    for i in range(4):
        result = str(num % 10) + result
        num = num / 10
    return result


print 'hello'
print 'fucking'
print 'world'

dir = 'E:/4_new'
mapping_file = open(dir+'/mappings.txt', 'w')
for i in range(5000):
    char_code = ImageChar()
    char_code.randChinese(4)
    index = get_name(i)
    char_code.save(dir+'/%s.jpg' % index)
    mapping_file.write(index+','+str(char_code.rotate_index)+'\n')
    print i