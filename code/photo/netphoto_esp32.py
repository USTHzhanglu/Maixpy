# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
import sensor, image, time
import network,socket,gc
perFrame=[0,0,320,240,27,0x7F800000,0x7F800000]
ssid="1234"
key="11111111"
def set_net():
    #wifi config
    from network_esp32 import wifi
    if wifi.isconnected() == False:
        for i in range(5):
            try:
                # Running within 3 seconds of power-up can cause an SD load error
                # wifi.reset(is_hard=False)
                wifi.reset(is_hard=True)
                print('try AT connect wifi...')
                wifi.connect(ssid, key)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())
    #A=net.ifconfig()#cheak ip address. Your sock addr should be same to this
    ADDR={}
    ADDR[0]=wifi.ifconfig()[2]
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

clock = time.clock()
sock = socket.socket()
sock.connect(set_net())
sock.settimeout(10)
set_img()

while(True):
    send_img(get_img(70))
    time.sleep_ms(100)
