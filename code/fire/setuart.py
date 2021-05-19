#please save txt as setuart.py and upload to k210
import time, network
from machine import UART
from fpioa_manager import fm
class setUART():
    def init():
        fm.register(7, fm.fpioa.UART1_TX, force=True)
        fm.register(6, fm.fpioa.UART1_RX, force=True)
        __class__.uart = UART(UART.UART1, 115200, timeout=1000, read_buf_len=8192)

    def _at_cmd(cmd="AT\r\n", resp="OK\r\n", timeout=20):
        __class__.uart.write(cmd) # "AT+GMR\r\n"
        time.sleep_ms(timeout)
        tmp = __class__.uart.read()
        # print(tmp)
        if tmp and tmp.endswith(resp):
            return True
        return False

    def setuart(baudrate=1152000, reply=5):
        __class__.init()
        for i in range(reply):
            print('set baudrate=%d...'%baudrate)
            time.sleep_ms(500) # at start > 500ms
            if __class__._at_cmd(timeout=500):
                break
        __class__._at_cmd()
        __class__._at_cmd('AT+UART_CUR=%d,8,1,0,0\r\n'%baudrate, "OK\r\n")#设置当前波特率，重启模块恢复到115200
if __name__ == "__main__":
    setUART.setuart()
    uart2 = UART(UART.UART1,1152000, timeout=1000, read_buf_len=10240)
    while(True):
        uart2.write("AT\r\n")
        B=uart2.read()
        print(B)
