# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(9, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time
import network,socket,gc
from setuart import setUART as SU
perFrame=[0,0,320,240,27,0x7F800000,0x7F800000]
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
    ADDR = ("{}".format(ADDR[0]), 1347)
    return ADDR
    #socket config end
def set_img():
    #sensor.config
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)
    #sensor.config end
def get_img(quality=70):
    img = sensor.snapshot()
    img = img.compress(quality)#压缩图片为jpg，质量为10%
    perFrame[1] = img.size()
    img_bytes = img.to_bytes() #转换图片为byte数组
    return img_bytes
def send_img(img_bytes):
    sendbuff=b''
    for i in perFrame:
        buff=i.to_bytes(4,'little')
        sendbuff=sendbuff+buff
    sendbuff=sendbuff+img_bytes
    sock.send(sendbuff)#以数组形式发送图片
    block = int(len(img_bytes)/2048)
#    for i in range(block):
#       sock.send(img_bytes[i*2048:(i+1)*2048])
 #      sock.send(img_bytes[block*2048:])
clock = time.clock()

sock = socket.socket()
sock.connect(set_net(2048000))
sock.settimeout(10)
set_img()

while(True):
    send_img(get_img(50))
