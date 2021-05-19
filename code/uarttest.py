# Untitled - By: Lithromantic - 周日 2月 7 2021
#注意，复用uart后，ide将无法使用
from fpioa_manager import fm
fm.register(7, fm.fpioa.UART1_TX, force=True)
fm.register(6, fm.fpioa.UART1_RX, force=True)
from machine import UART
import time
uart = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
uart.write("test repl2\r\n")
print(uart.read())
#print("test repl")
'''
if __name__ == "__main__":
   # at_cmd('+++')
    at_cmd(order,timeout=4000)
    at_cmd('AT+CIPMODE=1\r\n')
    at_cmd('AT+CIPSEND\r\n')
    '''
