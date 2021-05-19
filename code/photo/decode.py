# Untitled - By: Lithromantic - 周日 2月 7 2021
#注意，复用uart后，ide将无法使用
from fpioa_manager import fm
fm.register(9, fm.fpioa.UART1_TX, force=True)
fm.register(10, fm.fpioa.UART1_RX, force=True)
from machine import UART
import sensor, image, time,lcd
lcd.init(freq=15000000)
uart_A = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
img = []
clock = time.clock()
while(True):
        clock.tick()
        b=uart_A.read()
        if b!= None:
            print(b[5])
