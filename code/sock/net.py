# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,network
import struct
import socket
'''
ssid="1234"
key="11111111"

uart_A = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
net=network.ESP8285(uart_A)
net.connect(ssid, key)
'''
ADDR = ("192.168.137.1", 1347)
sock = socket.socket()
sock.connect(ADDR)
sock.settimeout(1)
img=b''
clock = time.clock()
while(True):
    clock.tick()
    sock.send("hello\n")
    while True:
        data = sock.recv(128)
        if len(data) == 0:
            break
        print("rcv:", len(data))
        img = img + data
    print(img)
