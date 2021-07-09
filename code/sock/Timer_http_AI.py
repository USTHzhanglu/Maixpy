# Untitled - By: Lithromantic - 周日 7月 4 2021

import sensor,lcd,image,time
import KPU as kpu
import gc, sys
class KPU_STATUS():
    is_waiting=0
    is_runing=1
    is_ok=2
    is_error=3
    status=is_error
    order=is_runing

class KPU_PARAMETER():
    img=None
    task=None
    anchor=(0.64, 0.67, 0.93, 0.97, 0.98, 1.06, 1.07, 1.17, 1.17, 1.3)
    code=None
    rect=None
    label = ["fire"]

class NET_PARAMETER():
    ssid="1234"
    key="11111111"
    uid="45df377e15b068b8c2ec930c22a784fb"
    topic="K210"
    method='POST'
    url='http://images.bemfa.com/upload/v1/upimages.php'
    data=None
    headers={"Content-Type":"image/jpg","Authorization": uid,"Authtopic":topic}
    img=None
    tm=None

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0x00,0xff,0xff))
    lcd.display(img)

def resize(memory=0x80000):
    from Maix import utils
    gc.collect()
    utils.gc_heap_size(memory)
    kpu.memtest()

def kpu_init(labels = None, model_addr="/sd/yolov2.kmodel"):
    p.task = kpu.load(model_addr)
    kpu.init_yolo2(p.task, 0.5, 0.3, 5, p.anchor)
    if not labels:
        with open('labels.txt','r') as f:
            exec(f.read())
    if not labels:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

def sensor_init(lcd_rotation=0, sensor_hmirror=True, sensor_vflip=True):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    #sensor.set_windowing((224,224))
    sensor.run(1)
    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

def network_init(baudrate=105200):
    from setuart import setUART as SU
    from fpioa_manager import fm
    from machine import UART
    import network
    fm.register(7, fm.fpioa.UART1_TX, force=True)
    fm.register(6, fm.fpioa.UART1_RX, force=True)
    SU.setuart(baudrate,1)
    uart = UART(UART.UART1,baudrate, timeout=1, read_buf_len=10240)
    net=network.ESP8285(uart)
    net.disconnect()
    print(net.isconnected())
    while net.isconnected() == False:
        print("connect...")
        try:
            net.connect(n.ssid, n.key)
        except Exception as e:
            pass

def request(method, url, data=None,headers={}):
    import usocket
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    else:
        raise ValueError("Unsupported protocol: " + proto)
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]
    s = usocket.socket(ai[0], ai[1], ai[2])
    s.settimeout(5)
    try:
        s.connect(ai[-1])
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if data:
            s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"\r\n")
        if data:
            s.write(data)
        s.close()
    except OSError:
        s.close()
        raise

def kpu_run():
    try:
        p.code = None
        img=image.Image(copy_to_fb=True)
        img=p.img.copy((48,8,224, 224))
        img.pix_to_ai()
        p.code = kpu.run_yolo2(p.task,img)
        if p.code!=None:
            max_area = 0
            max_i = 0
            for i, j in enumerate(p.code):
                a = j.w()*j.h()
                if a > max_area:
                    max_i = i
                    max_area = a
            p.rect=p.code[max_i].rect()
            p.img = p.img.draw_rectangle(p.rect)
            s.status=s.is_ok
        else:
            s.status=s.is_error
        lcd.display(p.img)
    except Exception as e:
        raise e

def kpu_waiting():
    try:
        lcd.display(p.img)
    except:
        pass

def kpu_post_code():
    p.img.compress(40)#压缩图片为jpg，质量为10%
    n.img=p.img.copy()
    n.data=n.img.to_bytes()
    print("begin")
    n.tm.start()
    request(method=n.method,url=n.url,data=n.data,headers=n.headers)
    n.tm.stop()
    print("ok")

def kpu_task():
    p.img = sensor.snapshot()
    kpu_run()
    if s.status == s.is_ok:
        kpu_post_code()

def timer_task(timer):
        p.img = sensor.snapshot()
        kpu_waiting()
        print(time.time())

def timer_init():
    from machine import Timer
    n.tm = Timer(Timer.TIMER0, Timer.CHANNEL0, \
    mode=Timer.MODE_PERIODIC, period=1000, \
    callback=timer_task, start=False,priority=1, div=0)


if __name__ == "__main__":
    s=KPU_STATUS()
    p=KPU_PARAMETER()
    n=NET_PARAMETER()
    network_init(baudrate=2048000)
    sensor_init(lcd_rotation=0, sensor_hmirror=True, sensor_vflip=True)
    kpu_init(labels=p.label, model_addr="/sd/yolov2.kmodel")
    timer_init()
    #resize(4096*1024)
    try:
        while True:
            kpu_task()
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
        n.tm.stop()
        if not p.task is None:
            kpu.deinit(p.task)
