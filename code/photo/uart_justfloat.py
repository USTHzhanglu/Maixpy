# Untitled - By: Lithromantic - 周日 2月 7 2021
#注意，复用uart后，ide将无法使用
from fpioa_manager import fm
fm.register(9, fm.fpioa.UART1_TX, force=True)
fm.register(10, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time
uart_A = UART(UART.UART1, 1152000, 8, 1, 0, timeout=1000, read_buf_len=4096)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
perFrame=[0,0,0,0,0]
prendFrame =[0x00, 0x00, 0x80, 0x7f,0x00, 0x00, 0x80, 0x7f]
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.compress(quality=80)#压缩图片为jpg，质量为10%
    perFrame[0] = 0
    perFrame[1] = img.size()
    perFrame[2] =img.width()   # 图片宽度
    perFrame[3] = img.height() # 图片高度
    perFrame[4] =27
    img_bytes = img.to_bytes() #转换图片为byte数组
    #####此处为vota+上位机的前导帧，使用其他接收时自行修改#####
    for i in perFrame:
        buff=i.to_bytes(4,'little')
        uart_A.write(buff,len(buff))
    uart_A.write(bytes(prendFrame),len(bytes(prendFrame)))
    ######################################################
    uart_A.write(img_bytes,img.size())#以数组形式发送图片
    print(img)
