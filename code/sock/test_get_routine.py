import socket
import network
import gc
import os
import lcd, image
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,network
import struct
import socket

ssid="1234"
key="11111111"

uart_A = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
net=network.ESP8285(uart_A)
net.connect(ssid, key)

sock = socket.socket()
addr = socket.getaddrinfo("dl.sipeed.com", 80)[0][-1]
sock.connect(addr)
sock.send('''GET /MAIX/MaixPy/assets/Alice.bmp HTTP/1.1
Host: dl.sipeed.com
cache-control: no-cache

''')

img = b""
sock.settimeout(5)
while True:
    data = sock.recv(4096)
    if len(data) == 0:
        break
    print("rcv:", len(data))
    img = img + data

print(len(img))
img = img[img.find(b"\r\n\r\n")+4:]
print(len(img))
print("save to /sd/Alice.bmp")
f = open("/sd/Alice.bmp","wb")
f.write(img)
f.close()
print("save ok")
print("display")
img = image.Image("/sd/Alice.bmp")
lcd.init()
lcd.display(img)
