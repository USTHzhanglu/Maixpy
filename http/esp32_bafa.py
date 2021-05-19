# Untitled - By: Lithromantic - 周二 3月 9 2021
from fpioa_manager import fm
import sensor, image, time,network
import socket
import urequests
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)
ssid="1234"
key="11111111"
uid="45df377e15b068b8c2ec930c22a784fb"
topic="K210"
method='POST'
url='http://images.bemfa.com/upload/v1/upimages.php'
data=None
headers={"Content-Type":"image/jpg","Authorization": uid,"Authtopic":topic}
def set_net():
    from network_esp32 import wifi
    if wifi.isconnected() == False:
        for i in range(5):
            try:
                # Running within 3 seconds of power-up can cause an SD load error
                # wifi.reset(is_hard=False)
                wifi.reset(is_hard=False)
                print('try AT connect wifi...')
                wifi.connect(ssid, key)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())
set_net()
while True:
    img=img = sensor.snapshot()
    img = img.compress(5)#压缩图片为jpg，质量为10%
    data=img.to_bytes()
    response = urequests.request(method=method,url=url,data=data,headers=headers)
    print(response.status_code)
    print(response.reason)
    parsed = response.json()
    print(parsed["url"])
