# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,network
import socket
from setuart import setUART as SU

ssid="1234"
key="11111111"

def set_net(baudrate=1152000):
    #wifi config

    SU.setuart(baudrate,1)
    uart = UART(UART.UART1,baudrate, timeout=1000, read_buf_len=10240)#创建外部可访问的uart
    net=network.ESP8285(uart)
    net.disconnect()
    net.connect(ssid, key)
    #A=net.ifconfig()#cheak ip address. Your sock addr should be same to this
    ADDR={}
    ADDR[0]=net.ifconfig()[2]
    print(ADDR[0])
    #wifi config end

    #socket config
    ADDR = ("{}".format(ADDR[0]), 80)
    #ADDR = (socket.getaddrinfo("http://192.168.137.1/hello/", 80)[0][-1])
    return ADDR
    #socket config end
#ADDR = (socket.getaddrinfo("http://192.168.137.1", 80)[0][-1])
sock = socket.socket()
sock.connect(set_net(1152000))
sock.settimeout(10)
'''
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
'''

post_request_info = b'''GET /hello/ HTTP/1.1
Host: localhost

'''
while (True):
    post_bytes=post_request_info
    print(post_bytes)
    sock.send(post_bytes)
    res = sock.recv(8092)
    #res=res.decode("utf-8")
    #res=str(res,"utf-8")
    print(res)
