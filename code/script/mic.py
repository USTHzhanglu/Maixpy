from Maix import MIC_ARRAY as mic
import lcd,time
import math
mic.init(i2s_d0=34, i2s_d1=8, i2s_d2=33, i2s_d3=9, i2s_ws=32, i2s_sclk=10,\
            sk9822_dat=7, sk9822_clk=35)#可自定义配置 IO
def get_mic_dir():
    AngleX=0
    AngleY=0
    AngleR=0
    Angle=0
    AngleAddPi=0
    mic_list=[]
    imga = mic.get_map()    # 获取声音源分布图像
    b = mic.get_dir(imga)   # 计算、获取声源方向
    for i in range(len(b)):
        if b[i]>=2:
            AngleX+= b[i]*math.sin(i*math.pi/6)
            AngleY+= b[i]*math.cos(i*math.pi/6)
    AngleX=round(AngleX,6) #计算坐标转换值
    AngleY=round(AngleY,6)
    if AngleY<0:AngleAddPi=180
    if AngleX<0 and AngleY > 0:AngleAddPi=360
    if AngleX!=0 or AngleY!=0: #参数修正
        if AngleY==0:
            Angle=90 if AngleX>0 else 270 #填补X轴角度
        else:
            Angle=AngleAddPi+round(math.degrees(math.atan(AngleX/AngleY)),4) #计算角度
        AngleR=round(math.sqrt(AngleY*AngleY+AngleX*AngleX),4) #计算强度
        mic_list.append(AngleX)
        mic_list.append(AngleY)
        mic_list.append(AngleR)
        mic_list.append(Angle)
    a = mic.set_led(b,(0,0,255))# 配置 RGB LED 颜色值
    return mic_list #返回列表，X坐标，Y坐标，强度，角度
while True:
    A=get_mic_dir()
    if A:
        print(A)
    time.sleep_ms(100)
