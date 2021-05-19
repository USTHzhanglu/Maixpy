# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,network
import socket
ssid="1234"
key="11111111"
'''
uart_A = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
net=network.ESP8285(uart_A)
net.connect(ssid, key)
print(net.ifconfig())
'''
ADDR = ("192.168.137.1", 80)
sock = socket.socket()
sock.connect(ADDR)
sock.settimeout(10)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

post_request_info = b'''POST /photo/ HTTP/1.1
Host: 127.0.0.1:80
FILENAME:JPG
Content-Type: application/multipart/form-data
Content-Length: '''
usrname=b'''

'''
while (True):
    img = sensor.snapshot()
    img = img.compress(quality=50)#压缩图片为jpg，质量为10%
    img_size=img.size()
    img_bytes=img.to_bytes()
    post_bytes=post_request_info+str(img_size)+usrname
    print(post_bytes)
    sock.send(post_bytes)
    block = int(len(img_bytes)/2048)
    for i in range(block):
       sock.send(img_bytes[i*2048:(i+1)*2048])
       sock.send(img_bytes[block*2048:])
    res = sock.recv(8096)
    print(res)
