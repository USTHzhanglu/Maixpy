from fpioa_manager import fm
import time
from Maix import GPIO
from machine import Timer

Timing_time = 0
distance = 0
start = time.ticks_us()

fm.register(22, fm.fpioa.GPIOHS0)
R = GPIO(GPIO.GPIOHS0,GPIO.IN, GPIO.PULL_UP)#HC_SR04的Echo引脚

fm.register(23, fm.fpioa.GPIO1)#HC_SR04的Trig引脚
T = GPIO(GPIO.GPIO1,GPIO.OUT)
T.value(0)

def HC_SR04 (pin_num):#外部中断回调函数
    global Timing_time,distance,start
    if R.value() == 1 and T.value() == 0:                  #判断是上升沿
        start = time.ticks_us()           #

    else:                                 #判断是下降沿
        Timing_time = time.ticks_diff(time.ticks_us(),start)
        distance = (Timing_time*0.034)/2 if 100<= Timing_time <=50000 else 'Out of distance'
           #计算距离CM,舍弃掉异常值
        print('distance:',distance)

    print(R.value(),Timing_time)
R.irq(HC_SR04,GPIO.IRQ_BOTH, GPIO.WAKEUP_NOT_SUPPORT,7)#外部引脚中断配置

while True:
    T.value(1)
    time.sleep_us(10)
    T.value(0)
    time.sleep_ms(1000)
