# PythonCollection  
This repository is used for store my python scripts and some python learning resource.

## Contents
[ImageEncryption](https://github.com/Zeacone/PythonCollection#ImageEncryption)

### ImageEncryption

#### Introduce
ImageCryption is a python script which can hide message to a picture(supported only PNG and gif), and then get message from the encryptioned picture.

#### Usage
First we open an image to encrypt message and resave a new image when finished by using function `resaveImage`.
```
from PIL import Image
image = Image.open('batman.png').convert('RGB')
new_image = resaveImage(image, 'This is a message.')
new_image.save('encrypt_batman.png')
```
Then we can just use function `getMessage` to print message.
```
encrypt_image = Image.open('encrypt_batman.png').convert('RGB')
print getMessage(crypt_image)
```
Or write message into file.
```
f = open('message.txt', 'w')
f.write(getMessage(crypt_image))
f.close()
f = open('message.txt')
files = f.readlines()
print files
f.close()
```