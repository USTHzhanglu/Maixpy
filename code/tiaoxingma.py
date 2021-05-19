import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA) # High Res!
sensor.set_windowing((320, 80)) # V Res of 80 == less work (40 for 2X the speed).
sensor.skip_frames(30)
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    codes = img.find_barcodes()
    for code in codes:
        img.draw_rectangle(code.rect(),color = (100, 255, 255),fill=True)
        print(code)
