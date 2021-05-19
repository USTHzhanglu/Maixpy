# 前言

用过esp系列单片机的童鞋都知道，esp的micropython提供的有一个webrepl模块，多好用就不用多说了。那么好用的东西，能在Maixpy上运行吗？答案是不行的，毕竟没有原生网络支持。但是请不要气馁，我们的Maixpy是可以拓展esp用的。既然能用WiFi，为什么不尝试着想些鬼点子呢？本贴我们就将通过Dock上板载的esp8285，实现伪webrepl。

警告⚠：由于开启了无线透传，网络功能将无法使用。如果要使用网络功能，请务必先执行至少一次repl.endrepl()

# 工具准备

1.Maix Dock，板载ESP8285至少连接过一次WiFi；

2.能开热点的电脑一台；

3.[虚拟串口软件](https://www.tastek.cn/productdownload/4/TASTEK_VCOM_SETUP.rar)or VOFA+；

4.跳线帽两个；

# 程序上手

## 原理

在ESP8285的AT命令中，有设置无线透传的命令。通过无线透传，可以将收发两方直接连接。通过虚拟串口，将网络层传来的消息转发到串口中，就能实现远程repl。

##  源码

```python
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
        print(tmp)
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
        __class__._at_cmd('AT+CIFSR\r\n')
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
        _A=__class__._at_cmd('AT+SAVETRANSLINK=0\r\n')
        print(_A)
if __name__ == "__main__":
    repl = webrepl(ip=ip,port=port,method=method)
    #repl.endrepl()
    repl.setrepl()
    #repl.scan()

```

## 上手-TCP

创建TCP无线透传前，需要先起一个服务器。这里以虚拟串口为例（VOFA+见以前帖子），添加串口，网络协议选择TCP Server，本地端口填写任意数（注意不要冲突）

![image-20210510210925371](C:\Users\Lithromantic\AppData\Roaming\Typora\typora-user-images\image-20210510210925371.png)

修改网络参数：

```python
ip="192.168.137.1",填写热点ip，或者使用repl.scan()查找ip
port="6666"，填写虚拟串口的本地端口
method="TCP"
```

可选参数：

```python
keep_alive:[0-7200],TCP保持间隔
TX，非dock板外接esp的TX0引脚数
RX，非dock板外接esp的RX0引脚数

```

初始化：`repl = webrepl(ip=ip,port=port,method=method)`   

启动：`repl.setrepl()`

停止：`repl.endrepl()`

## 上手-UDP

创建UDP无线透传前，需要`repl.scan()`本机ip，并设置local_port。

参考如下：

```python
local_port="8266"
method="UDP"
repl = webrepl(ip=ip,port=port,method=method)
repl.scan()
>>>b'AT+CIFSR\r\n+CIFSR:STAIP,"192.168.137.52"\r\n
```

记录下本机IP`192.168.137.52`。

这里以虚拟串口为例，添加串口，网络协议选择UDP，本地端口填写任意数（注意不要冲突）,目标IP填写上述IP,本目标端口填写local_port。

![image-20210511172714522](C:\Users\Lithromantic\AppData\Roaming\Typora\typora-user-images\image-20210511172714522.png)

启动：`repl.setrepl()`

停止：`repl.endrepl()`

# 效果演示

## 虚拟串口

使用虚拟串口后，你可以使用任何使用串口的软件进行连接。如果无反应，尝试下复位。请先通过跳线帽连接4<-->6,5<--->7引脚。

XCOM

![image-20210511174527937](C:\Users\Lithromantic\AppData\Roaming\Typora\typora-user-images\image-20210511174527937.png)

VOFA+(网络调试助手)

网络调试助手不需要设置虚拟串口，直接配置数据接口，连接即可。

![image-20210511175009224](C:\Users\Lithromantic\AppData\Roaming\Typora\typora-user-images\image-20210511175009224.png)