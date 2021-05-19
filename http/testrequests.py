# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,network
import socket
import urequests
from setuart import setUART as SU
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)
ssid="1234"
key="11111111"
method='POST'
url="http://192.168.137.1/photo/"
data=None
headers={'FILENAME':'JPG'}
def set_net(baudrate=1152000):
    #wifi config

    SU.setuart(baudrate,1)
    uart = UART(UART.UART1,baudrate, timeout=1000, read_buf_len=10240)
    net=network.ESP8285(uart)
    net.disconnect()
    net.connect(ssid, key)
#set_net(4096000)
while True:
    img=img = sensor.snapshot()
    img = img.compress(100)#压缩图片为jpg，质量为10%
    data=img.to_bytes()
    response = urequests.request(method=method,url=url,data=data,headers=headers)
    print(response.status_code)
    print(response.reason)
    print(response.text)


