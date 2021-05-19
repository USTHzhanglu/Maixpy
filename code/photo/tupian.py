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

clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.compress(quality=80)#压缩图片为jpg，质量为10%
    IMG_ID = 0
    IMG_SIZE = img.size()
    IMG_WIDTH =img.width()   # 图片宽度
    IMG_HEIGHT = img.height() # 图片高度
    IMG_FORMAT =27
    img_bytes = img.to_bytes() #转换图片为byte数组
    #####此处为vota+上位机的前导帧，使用其他接收时自行修改#####
    uart_A.write("image:%d,%d,%d,%d,%d\n"%(
            IMG_ID,     # 此ID用于标识不同图片通道
            IMG_SIZE,    # 图片数据大小
            IMG_WIDTH,   # 图片宽度
            IMG_HEIGHT, # 图片高度
            IMG_FORMAT# 图片格式
            )
            )
    ######################################################
    uart_A.write(img_bytes,IMG_SIZE)#以数组形式发送图片
   # time.sleep_ms(50)
    print(img)

