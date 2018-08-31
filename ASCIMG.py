from PIL import Image, ImageDraw, ImageFont
import time


WIDTH = 7
HEIGHT = 8
CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWYZ1234567890!#%^&*`~-=+;:\'\",<.>/? '
TTF = 'monaco.ttf'
useful = [0]*len(CHARS)

BIT = [1]
FONT = []
FONTHASH = []


def Hash(img):
    # w, h = img.size
    # pixels = list(img.getdata())
    # diff = list()
    # last = 0
    # for y in range(h):
    #     for x in range(1, w):
    #         if pixels[last] < pixels[last+1]:
    #             diff.append('0')
    #         else:
    #             diff.append('1')
    #         last += 1
    #     last += 1
    # return int("".join(diff), 2)

    w, h = img.size
    pixels = list(img.getdata())
    diff = 0
    last = 0
    for y in range(h):
        for x in range(1, w):
            if pixels[last] >= pixels[last+1]:
                diff += BIT[last]
            last += 1
        last += 1
    return diff


def Disance(a, b):
    return bin(a ^ b).count('1')


def Match(hsh):
    it = 0
    dis = 0x3f3f
    for i, ele in enumerate(FONTHASH):
        tem = Disance(ele, hsh)
        if(tem < dis):
            dis = tem
            it = i
    return it


def Img2ch(img):
    w, h = img.size
    ch = Image.new("L", (w, h), color="white")
    for y in range(0, h, HEIGHT):
        for x in range(0, w, WIDTH-1):
            hsh = Hash(img.crop((x-1, y, x+WIDTH-1, y+HEIGHT)))
            it = Match(hsh)
            useful[it] += 1
            ch.paste(FONT[it], (x-1, y))
    return ch


def InitFont():
    for i in range(1, 64):
        BIT.append(BIT[i-1]*2)
    for ch in CHARS:
        img = Image.new("L", (WIDTH, HEIGHT), color="white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(TTF, 10)
        draw.text((1, -2), ch, font=font)
        FONT.append(img)
        FONTHASH.append(Hash(img))


# TESTIMG = ['testimg0.jpg', 'testimg1.jpg',
#            'testimg2.jpg', 'testimg3.jpg', 'testimg4.jpg']


TESTIMG = ['testimg1.jpg',
           'testimg2.jpg', 'testimg3.jpg', 'testimg4.jpg']

if __name__ == '__main__':

    InitFont()
    start = time.process_time()
    for f in TESTIMG:

        img = Image.open('./'+f)
        img = img.convert('L')
        ch = Img2ch(img)
        ch.save('./'+f+'.png', 'png')
    print(time.process_time()-start)

    # print(useful)

    exit(0)
