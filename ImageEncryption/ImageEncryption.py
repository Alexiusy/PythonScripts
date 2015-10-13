#coding:utf-8

__author__ = "Zeaconeus"
__version__ = "1.0"

from PIL import Image

def hidden_message(image, message):
	message_length = len(message)
    if message_length == 0:
		raise ValueError('There is no message!')
    if message_length * 3 > len(image.getdata()):
        raise ValueError('The message is too long to hidden in image.')

    # 获取图片数据，保存在迭代器之中
    image_data = iter(image.getdata())

    for i in xrange(message_length):
        binaryCode = ord(message[i])
        # 将三组RGB数值（即三个像素一组）生成一个迭代器
        container = [RGB & ~1 for RGB in image_data.next()[:3] + image_data.next()[:3] + image_data.next()[:3]]
        
        # 最多八步即可将可显示的ASCII码完全转化为二进制，将RGB迭代器前8位作为标识位
        for j in xrange(7, -1, -1):
            # 奇数 & 1 == 1， 偶数 & 1 == 0。
            # 偶数 | 1 == 奇数（偶数 + 1）， 偶数 | 0 == 偶数。
            # 因此此处能够区分字符ASCII码的二进制，通过判断RGB值的奇偶即可得出二进制数字串
             container[j] |= (binaryCode & 1) 
             binaryCode >>= 1

         # 需要隐藏的信息结束，在RGB值设置结束标志位，便于解密时判断。
        if i == message_length - 1:
             container[-1] |= 1

        container = tuple(container)
        yield container[0:3]
        yield container[3:6]
        yield container[6:9]

def new_image(image, message):
    width, height = image.size
    (x, y) = (0, 0)
    for pixel in hidden_message(image, message):
        image.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1
    return image


# 解密部分：
    # 1.按照加密时的方法反向解密数据
    # 2.拼接字符，完成信息的解密

def get_charactor(image):
    image_data = iter(image.getdata())
    while True:
        binaryCode = 0
        pixels = list(image_data.next()[:3] + image_data.next()[:3] + image_data.next()[:3])
        for c in xrange(7):
            binaryCode |= pixels[c] & 1
            binaryCode <<= 1
        binaryCode |= pixels[7] & 1

        # 返回字符生成器
        yield chr(binaryCode)

        # 结束标识
        if pixels[-1] & 1:
            break

def get_message(image):
    return ''.join(get_charactor(image))

image = Image.open('batman.png').convert('RGB')
new_image = new_image(image, '1234423')
new_image.save('batman1.png')

crypt_image = Image.open('batman1.png').convert('RGB')
# print get_message(crypt_image)

f = open('message.txt', 'w')
f.write(get_message(crypt_image))
f.close()
f = open('message.txt')
files = f.readlines()
print files
f.close()
