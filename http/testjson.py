# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,network
import socket
import urequests
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
from setuart import setUART as SU
'''
ssid="1234"
key="11111111"
uid="45df377e15b068b8c2ec930c22a784fb"
topic="K210"
method='POST'
url='http://images.bemfa.com/upload/v1/upimages.php'
data=None
headers={"Content-Type":"image/jpg","Authorization": uid,"Authtopic":topic}
'''
'''
def set_net(baudrate=1152000):
    SU.setuart(baudrate,1)
    uart = UART(UART.UART1,baudrate, timeout=1000, read_buf_len=10240)
    net=network.ESP8285(uart)
    net.disconnect()
    net.connect(ssid, key)
set_net(1152000)
'''
while True:
    #img=img = sensor.snapshot()
    #img = img.compress(100)#压缩图片为jpg，质量为10%
    #data=img.to_bytes()
    response = urequests.get("http://jsonplaceholder.typicode.com/albums/1")
    print(response.status_code)
    print(response.reason)
    parsed = response.json()
    print(parsed)

