import utime,lcd,image
from Maix import GPIO
from Maix import FPIOA
from machine import Timer
num=0
status=''
def celiang(pin_num):
    global num,status
    print(xinhao.value())
    if xinhao.value()==0:
        status="high"
        print("按下")
    if xinhao.value()==1 and status=="high":
        status="low"
        num = num + 1
        print("松开")
fpioa = FPIOA()
fpioa.set_function(14,fpioa.GPIOHS0)
xinhao = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)
xinhao.irq(celiang,GPIO.IRQ_BOTH,GPIO.WAKEUP_NOT_SUPPORT,7)
def timer_task(timer):
        global num
        #print(num)
        num=0

def timer_init():
    from machine import Timer,PWM
    tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
    ch = PWM(tim, freq=10, duty=50, pin=14)
timer_init()
while(True):
    pass
