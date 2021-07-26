
try:
    import os, Maix, lcd, image,gc,sys
    gc.collect()
    lcd.init()
    loading = image.Image(size=(lcd.width(), lcd.height()))
    loading.draw_rectangle((0, 0, lcd.width(), lcd.height()), fill=True, color=(255, 0, 0))
    info = "Welcome to MaixPy"
    loading.draw_string(int(lcd.width()//2 - len(info) * 5), (lcd.height())//4, info, color=(255, 255, 255), scale=2, mono_space=0)
    v = sys.implementation.version
    vers = 'V{}.{}.{} : maixpy.sipeed.com'.format(v[0],v[1],v[2])
    loading.draw_string(int(lcd.width()//2 - len(info) * 6), (lcd.height())//3 + 20, vers, color=(255, 255, 255), scale=1, mono_space=1)
    tf = None
    try:
            os.listdir("/sd/.")
    except Exception as e:
        tf ="SDcard not mount,using flash!"
        loading.draw_string(int(lcd.width()//2 - len(info) * 7), (lcd.height())//2 + 10, tf, color=(255, 255, 255), scale=1, mono_space=1)
    if not tf:
        tf ="SDcard is mount,using sd!"
        loading.draw_string(int(lcd.width()//2 - len(info) * 6), (lcd.height())//2 + 10, tf, color=(255, 255, 255), scale=1, mono_space=1)
    lcd.display(loading)
finally:
    del loading, v, info, vers
    gc.collect()
