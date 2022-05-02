# Untitled - By: Lithromantic - 周五 3月 5 2021

import sensor, image, time,lcd
lcd.init(type=5,freq=50*1000*1000,lcd_type=3)
def Bytes_to_img(imgdir):
    _imgdir=imgdir
    _jpeg_buff={}
    with open(_imgdir,'rb') as f:
        _jpeg_buff=f.read()
    _image = image.Image(_jpeg_buff, from_bytes = True)
    return _image
while(True):
    img=Bytes_to_img("图片1.jpg")

    print(img)
