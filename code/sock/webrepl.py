import time, network
from machine import UART
from fpioa_manager import fm
import socket
ip="192.168.137.1"
port="6666"
local_port="8266"
method="UDP"
class webrepl():
    def __init__(self,ip,port,method,keep_alive=100,local_port='8266',TX=7,RX=6):
        self._ip = ip
        self._port = port
        self._method = method
        self._keep_alive=keep_alive
        self._local_port=local_port
        self._TX=TX
        self._RX=RX


    def init(self):
        fm.register(self._TX, fm.fpioa.UART1_TX, force=True)
        fm.register(self._RX, fm.fpioa.UART1_RX, force=True)
        __class__.uart = UART(UART.UART1, 115200, timeout=1000, read_buf_len=8192)
    def _at_cmd(cmd="AT\r\n", resp="OK\r\n", timeout=20):
        print(cmd)
        __class__.uart.write(cmd) # "AT+GMR\r\n"
        time.sleep_ms(timeout)
        tmp = __class__.uart.read()
        #print(tmp)
        if tmp and tmp.endswith(resp):
            return True
        return False
    def scan(self):
        __class__.init(self)
        __class__._at_cmd('+++')
        for i in range(4):
            time.sleep_ms(500) # at start > 500ms
            if __class__._at_cmd(timeout=500):
                break
        __class__.uart.write('AT+CIFSR\r\n')
        _A = __class__.uart.read()
        if _A !=None:
            print(_A.decode())
    def setrepl(self):
        __class__.init(self)
        __class__._at_cmd('+++')
        for i in range(4):
            print('try set repl@'+self._ip+':'+self._port+'by'+self._method)
            time.sleep_ms(500) # at start > 500ms
            if __class__._at_cmd(timeout=500):
                break
        __class__._at_cmd()
        if self._method == "TCP":
            _A=__class__._at_cmd('AT+SAVETRANSLINK=1,"'+\
                              self._ip+'",'+\
                              self._port+',"'+\
                              self._method+'",'+\
                              self._keep_alive+'\r\n',timeout=1000)
        else:
            _A=__class__._at_cmd('AT+SAVETRANSLINK=1,"'+\
                              self._ip+'",'+\
                              self._port+',"'+\
                              self._method+'",'+\
                              self._local_port+'\r\n',timeout=1000)
        print(_A)
    def endrepl(self):
        __class__.init(self)
        __class__._at_cmd('+++')
        for i in range(4):
            print('try end')
            time.sleep_ms(500) # at start > 500ms
            if __class__._at_cmd(timeout=500):
                break
        _A=__class__._at_cmd('AT+SAVETRANSLINK=0\r\n')#设置当前波特率，重启模块恢复到115200
        print(_A)
if __name__ == "__main__":
    repl = webrepl(ip=ip,port=port,method=method)
    #repl.endrepl()
    #repl.setrepl()
    repl.scan()
