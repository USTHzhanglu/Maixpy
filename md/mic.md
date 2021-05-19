# 前言

最近搞到块麦克风阵列，上面有12个会发光的小灯，能显示声音方向。还能通过lcd显示彩虹图。

<img src="https://maixpy.sipeed.com/maixpy/assets/hardware/module/mic_array_taobao.jpg" style="zoom:50%;" />

但是实际应用总感觉缺了点啥。通过查看例程，发现返回的有个12元素的数组，

`(0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0)`

每个元素∈[0,15]，正好对应了12个小灯，猜想[0,15 ]代表了声音强度。有方位，有强度，就很容易想到
$$
z=x+iy和r=sinθ+icosθ
$$
通过向量计算，就可以合成出声音方位和强度。

## 坐标变换

麦克风阵列的十二个小灯，正好将一个⚪等分为12份。~~~十二等分的花嫁？~~~

![img](https://mc.dfrobot.com.cn/data/attachment/forum/202104/08/185823p0hjtfukaaho2haq.png)

角间距π/6。将Y轴设为0°，则小灯到Y轴的夹角为i*π/6,设声音强度为r，则第i个小灯方向的声音可以分解为：
$$
AngleX[i]= r[i]*sin(i*π/6)
$$

$$
AngleY[i]= r[i]*cos(i*π/6)
$$



合成为：
$$
θ[i]=arctan(AngleX[i]/AngleY[i])
$$

$$
AngleR[i]^2=AngleX[i]^2+AngleY[i]^2
$$

由向量加法公式：
$$
A(X1，Y1) B(X2，Y2)，A + B=（X1+X2，Y1+Y2）
$$
得合成公式：
$$
AngleX=∑_i^nAngleX[i]
$$

$$
AngleY=∑_i^nAngleY[i]
$$

$$
AngleR=∑_i^nAngleR[i]^{1/2}
$$

通过反三角函数，算出：
$$
θ=arctan(AngleX/AngleY)
$$
这样就算出了声音方向θ及强度AngleR

## 代码实现

1.获取AngleX,AngleY.遍历list[b]，求出有效值。过高的精度会导致AngleX,AngleY在无限趋近于0时异常，所以截取6位小数。

```python
import math
AngleX=0 #初始化
AngleY=0
imga = mic.get_map()    # 获取声音源分布图像
b = mic.get_dir(imga)   # 计算、获取声源方向
for i in range(len(b)):
    if b[i]>=1: #去除干扰和非零值
        AngleX+= b[i]*math.sin(i*math.pi/6)
        AngleY+= b[i]*math.cos(i*math.pi/6)
AngleX=round(AngleX,6) #计算坐标转换值
AngleY=round(AngleY,6)
```

2.计算θ及AngleR。同样截取有限小数。通过`math.atan()`计算弧度，通过`math.degrees()`转为角度。返回值∈(-90,90)

```python
           Angle=round(math.degrees(math.atan(AngleX/AngleY)),4) #计算角度
AngleR=round(math.sqrt(AngleY*AngleY+AngleX*AngleX),4) #计算强度
```

## 参数修正

通过上述计算出的参数，范围∈(-90,90),并不能满足实际需要，并且在X轴时，由于AngleY=0，还会导致计算错误。所以我们要进行一系列修正：

​	1.修正X轴参数：

```
if AngleY==0:
    Angle=90 if AngleX>0 else 270 #填补X轴角度
```

 	2.根据AngleX,AngleY判断象限并修正角度：

```
AngleAddPi=0
if AngleY<0:AngleAddPi=180
if AngleX<0 and AngleY > 0:AngleAddPi=360  Angle=AngleAddPi+round(math.degrees(math.atan(AngleX/AngleY)),4) #计算角度
```

## 封装函数

将程序片段封装好后，便于在其他地方使用。

```python
def get_mic_dir():#在使用前要先init mic
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
```

## 例程



```python
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
    print(get_mic_dir())
    time.sleep_ms(100)

```

输出：

```shell
MicroPython v0.6.2-15-g0118a9a77 on 2021-01-12; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>> 

>>> Microphone Array Arithmetic, Developed by Canaan, Port by Sipeed
[14.02628, 19.29423, 23.8538, 36.0159]
[6.696152, 5.598076, 8.7279, 50.1039]
[15.02628, 15.02628, 21.2504, 45.0]
[4.0, 6.928204, 8.0, 30.0]
[25.3923, -6.000002, 26.0916, 103.2947]
```

