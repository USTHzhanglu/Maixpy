import sensor,lcd,image,time
import KPU as kpu
import gc, sys
class KPU_STATUS():
    is_waiting=0
    is_runing=1
    is_ok=2
    is_error=3
    status=is_error
    order=is_waiting

class KPU_PARAMETER():
    img=None
    task=None
    anchor=(0.64, 0.67, 0.93, 0.97, 0.98, 1.06, 1.07, 1.17, 1.17, 1.3)
    code=None
    rect=None
    label = ["fire"]
    sock=None

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

def uart_init():
    from machine import UART
    from fpioa_manager import fm
    fm.register(9, fm.fpioa.UART1_TX, force=True)
    fm.register(8, fm.fpioa.UART1_RX, force=True)
    p.sock = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

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
def kpu_get_order():
    read_buf=p.sock.read()
    if read_buf!=None:
        print(read_buf)
        if "run" in read_buf:
            s.order=s.is_runing
            p.sock.write("ok\r\n")
        elif "stop" in read_buf:
            s.order=s.is_waiting
            p.sock.write("ok\r\n")
        else:
            p.sock.write("error\r\n")

def kpu_post_code():
    value=str(p.code[0].value())
    print(value)
    p.sock.write(value+"\r\n")
def kpu_task():
    p.img = sensor.snapshot()
    if s.order == s.is_waiting:
        kpu_waiting()
        kpu_get_order()
    elif s.order==s.is_runing and s.status==s.is_error:
        kpu_run()
        kpu_get_order()
    elif s.order==s.is_runing and s.status==s.is_ok:
        kpu_post_code()
        kpu_run()
        kpu_get_order()




if __name__ == "__main__":
    s=KPU_STATUS()
    p=KPU_PARAMETER()
    sensor_init(lcd_rotation=0, sensor_hmirror=True, sensor_vflip=True)
    kpu_init(labels=p.label, model_addr="/sd/yolov2.kmodel")
    uart_init()
   #resize(2048*2048)
    try:
        while True:
            kpu_task()
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
        if not p.task is None:
            kpu.deinit(p.task)
