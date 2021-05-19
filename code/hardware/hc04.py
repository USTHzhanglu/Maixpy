from fpioa_manager import fm
import time
from Maix import GPIO
from machine import Timer
Timing_time = 0
distance = 0
start = 0
fm.register(22, fm.fpioa.GPIOHS0)
R = GPIO(GPIO.GPIOHS0,GPIO.IN, GPIO.PULL_UP)#HC_SR04的Echo引脚
fm.register(23, fm.fpioa.GPIO1)#HC_SR04的Trig引脚
T = GPIO(GPIO.GPIO1,GPIO.OUT)
T.value(0)
def on_timer(timer):
    global start
    start+=1

def HC_SR04 (pin_num):#外部中断回调函数
    global Timing_time,distance,start
    if R.value() == 1 and T.value() == 0:                  #判断是上升沿
        start=0         #
    else:
        Timing_time = start
        distance = (Timing_time*0.34)/2   #计算距离CM
        print('distance:',distance)
    print(R.value(),start)
tim = Timer(0,0, mode=Timer.MODE_PERIODIC, period=10, unit=Timer.UNIT_US, callback=on_timer, priority=1 ,arg=None, start=True)
R.irq(HC_SR04,GPIO.IRQ_BOTH, GPIO.WAKEUP_NOT_SUPPORT,1)#外部引脚中断配置
while True:
    T.value(1)
    time.sleep_us(10)
    T.value(0)
    time.sleep_ms(1000)
