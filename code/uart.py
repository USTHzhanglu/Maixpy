# Untitled - By: Lithromantic - 周日 2月 7 2021
#注意，复用uart后，ide将无法使用
from fpioa_manager import fm
fm.register(7, fm.fpioa.UART1_TX, force=True)
fm.register(6, fm.fpioa.UART1_RX, force=True)
from machine import UART
import time,network
uart = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
'''
ssid="1234"
key="11111111"
net=network.ESP8285(uart)
net.connect(ssid, key)
ADDR={}
ADDR[0]=net.ifconfig()[2]
'''
#order=b'AT+CIPSTART="TCP","'+ADDR[0]+'",1234\r\n'
autoorder=b'AT+SAVETRANSLINK=1,"192.168.137.1",1234,"TCP",100\r\n'
def at_cmd(cmd="AT\r\n", resp="OK\r\n", timeout=20):
    uart.write(cmd) # "AT+GMR\r\n"
    time.sleep_ms(timeout)
    tmp = uart.read()
    #print(tmp)
    if tmp and tmp.endswith(resp):
        return True
    return False

at_cmd(autoorder,timeout=4000)
repl=UART.set_repl_uart(uart)
repl.init(115200, 8, None, 1, read_buf_len=2048)
#print("test repl")
'''
if __name__ == "__main__":
   # at_cmd('+++')
    at_cmd(order,timeout=4000)
    at_cmd('AT+CIPMODE=1\r\n')
    at_cmd('AT+CIPSEND\r\n')
    '''
