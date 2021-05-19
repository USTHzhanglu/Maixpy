import sensor,image,lcd,time
import KPU as kpu
import _thread
return_meg=['cheak']
WARNING={'cheak':'cheaking','unmask':'please mask','masks':'take off mask and waiting FACE cheak'}
def setsenor():
    lcd.init(freq=15000000)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    sensor.set_vflip(1)
    sensor.run(1)
def loadmodel():
    global return_meg
    classes = ['unmask','masks']
    status=0
    task = kpu.load("/sd/mask2.kmodel")
    anchor = (0.64, 0.67, 0.93, 0.97, 0.98, 1.06, 1.07, 1.17, 1.17, 1.3)
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
    while status==0:
        img = sensor.snapshot()
        code = kpu.run_yolo2(task, img)
        status = 1 if code else 0
        if code:
            for i in code:
                a=img.draw_rectangle(i.rect())
                a = lcd.display(img)
                for i in code:
                    lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                    lcd.draw_string(i.x(), i.y()+12, '%.3f'%i.value(), lcd.RED, lcd.WHITE)
                    return_meg=[classes[i.classid()],'%.3f'%i.value()]
        else:
         lcd.display(img)
         lcd.draw_string(50,10,'cheaking', lcd.RED,lcd.WHITE)
    kpu.deinit(task)
def facemodel():
    global return_meg
    classes = ['people','nopeople']
    status=0
    task = kpu.load("/sd/face.kmodel")
    anchors = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchors)
    sensor.set_framesize(sensor.QVGA)
    while True:
        img = sensor.snapshot()
        objects = kpu.run_yolo2(task, img)
        status = 1 if objects else 0
        if objects:
            for i in objects:
                a=img.draw_rectangle(i.rect())
                a = lcd.display(img)
                for i in objects:
                    lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
        else:
         lcd.display(img)
         lcd.draw_string(50,10,'take off mask and waiting FACE cheak', lcd.RED,lcd.WHITE)
    kpu.deinit(task)
if __name__ == "__main__":
    _thread.start_new_thread(setsenor(),(0,))
    _thread.start_new_thread(loadmodel(),(1,))
    while True:
        img = sensor.snapshot()
        lcd.display(img)
        lcd.draw_string(50,10, WARNING[return_meg[0]], lcd.RED,lcd.WHITE)
        if return_meg[0] =='masks':
            _thread.start_new_thread(facemodel(),(1,))
            return_meg[0]='unmask'

