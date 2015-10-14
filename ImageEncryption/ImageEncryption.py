#coding:utf8

__author__ = "Zeacone"
__version__ = "1.0"

from PIL import Image

"""
Encryption
"""

def encryptionMessage(image, message):
	image_data = image.getdata()
	message_length = len(message)
	if message_length == 0:
		raise ValueError('No message.')
	if message_length * 3 > len(image_data):
		raise ValueError('Message is too long.')

	# Put image data into an iterator.
	image_data_iterator = iter(image_data)

	for i in xrange(message_length):
		ASCII = ord(message[i])

		# Eight bits binary code present one character, so we need three pixels to save one character.
		# Serilize all rgb number to be even(Simply make first bit be 0).
		container = [rgb & ~1 for rgb in image_data_iterator.next()[:3] + image_data_iterator.next()[:3] + image_data_iterator.next()[:3]]

		# Only eight steps to convert a decimal number to binary.
		# ① odd & 1 = 1, even & 1 = 0, get 0 or 1; ② even | 1 = even + 1, even | 0 = even, get an decimal number.
		for j in xrange(7, -1, -1):
			container[j] |= (ASCII & 1)
			ASCII >>= 1

		# The ninth bit is empty, so we can put finish flag into it.
		if i == message_length - 1:
			container[-1] |= 1

		container = tuple(container)
		yield container[0:3]
		yield container[3:6]
		yield container[6:9]

def resaveImage(image, message):
	width, height = image.size
	(x, y) = (0, 0)
	for pixel in encryptionMessage(image, message):
		image.putpixel((x, y), pixel)
		if x == width - 1:
			x = 0
			y += 1
		else:
			x += 1
	return image


"""
Decryption
"""

def getCharacter(image):
    image_data = iter(image.getdata())
    while True:
        binaryCode = 0
        pixels = list(image_data.next()[:3] + image_data.next()[:3] + image_data.next()[:3])
        for c in xrange(7):
            binaryCode |= pixels[c] & 1
            binaryCode <<= 1
        binaryCode |= pixels[7] & 1

        # Return character generater.
        yield chr(binaryCode)

        # Finish flag.
        if pixels[-1] & 1:
            break

def getMessage(image):
	return ''.join(getCharacter(image))

