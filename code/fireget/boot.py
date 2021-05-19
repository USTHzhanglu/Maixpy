'''
    Gimbal demo with classical PID support,
    @usage Change parameters at the start of main according to your hardware
           like camera and lcd direction, PID parameters etc.

    @update https://github.com/sipeed/MaixPy_scripts
    @author neucrack@sipeed
    @license MIT
'''


import time, sys
from machine import Timer,PWM
from math import pi
from machine import UART
class WARNING:
    def __init__(self,IO=14):
        self._IO = IO
        from fpioa_manager import fm
        from Maix import GPIO
        fm.register(self._IO, fm.fpioa.GPIO1)
        self._T = GPIO(GPIO.GPIO1,GPIO.OUT)

    def warning(self,sw):
        self._T.value(sw)
class Servo:
    def __init__(self, pwm, dir=50, duty_min=2.5, duty_max=12.5):
        self.value = dir
        self.pwm = pwm
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty_range = duty_max -duty_min
        self.enable(True)
        self.pwm.duty(self.value/100*self.duty_range+self.duty_min)

    def enable(self, en):
        if en:
            self.pwm.enable()
        else:
            self.pwm.disable()

    def dir(self, percentage):
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        self.pwm.duty(percentage/100*self.duty_range+self.duty_min)

    def drive(self, inc):
        self.value += inc
        if self.value > 100:
            self.value = 100
        elif self.value < 0:
            self.value = 0
        self.pwm.duty(self.value/100*self.duty_range+self.duty_min)

class PID:
    _kp = _ki = _kd = _integrator = _imax = 0
    _last_error = _last_t = 0
    _RC = 1/(2 * pi * 20)
    def __init__(self, p=0, i=0, d=0, imax=0):
        self._kp = float(p)
        self._ki = float(i)
        self._kd = float(d)
        self._imax = abs(imax)
        self._last_derivative = None

    def get_pid(self, error, scaler):
        tnow = time.ticks_ms()
        dt = tnow - self._last_t
        output = 0
        if self._last_t == 0 or dt > 1000:
            dt = 0
            self.reset_I()
        self._last_t = tnow
        delta_time = float(dt) / float(1000)
        output += error * self._kp
        if abs(self._kd) > 0 and dt > 0:
            if self._last_derivative == None:
                derivative = 0
                self._last_derivative = 0
            else:
                derivative = (error - self._last_error) / delta_time
            derivative = self._last_derivative + \
                                     ((delta_time / (self._RC + delta_time)) * \
                                        (derivative - self._last_derivative))
            self._last_error = error
            self._last_derivative = derivative
            output += self._kd * derivative
        output *= scaler
        if abs(self._ki) > 0 and dt > 0:
            self._integrator += (error * self._ki) * scaler * delta_time
            if self._integrator < -self._imax: self._integrator = -self._imax
            elif self._integrator > self._imax: self._integrator = self._imax
            output += self._integrator
        return output

    def reset_I(self):
        self._integrator = 0
        self._last_derivative = None

class Gimbal:
    def __init__(self, pitch, pid_pitch, roll=None, pid_roll=None, yaw=None, pid_yaw=None):
        self._pitch = pitch
        self._roll = roll
        self._yaw = yaw
        self._pid_pitch = pid_pitch
        self._pid_roll = pid_roll
        self._pid_yaw = pid_yaw

    def set_out(self, pitch, roll, yaw=None):
        pass

    def run(self, pitch_err, roll_err=50, yaw_err=50, pitch_reverse=False, roll_reverse=False, yaw_reverse=False):
        out = self._pid_pitch.get_pid(pitch_err, 1)
        # print("err: {}, out: {}".format(pitch_err, out))
        if pitch_reverse:
            out = - out
        self._pitch.drive(out)
        if self._roll:
            out = self._pid_roll.get_pid(roll_err, 1)
            if roll_reverse:
                out = - out
            self._roll.drive(out)
        if self._yaw:
            out = self._pid_yaw.get_pid(yaw_err, 1)
            if yaw_reverse:
                out = - out
            self._yaw.drive(out)


if __name__ == "__main__":
    '''
        servo:
            freq: 50 (Hz)
            T:    1/50 = 0.02s = 20ms
            duty: [0.5ms, 2.5ms] -> [0.025, 0.125] -> [2.5%, 12.5%]
        pin:
            IO10 <--> pitch
            IO11 <--> roll
    '''
    init_pitch = 0       # init position, value: [0, 100], means minimum angle to maxmum angle of servo
    init_roll = 50        # 50 means middle
    sensor_hmirror = False
    sensor_vflip = False
    lcd_rotation = 2
    lcd_mirror = True
    pitch_pid = [0.23, 0, 0.015, 0]  # P I D I_max
    roll_pid  = [0.23, 0, 0.015, 0]  # P I D I_max
    target_err_range = 10            # target error output range, default [0, 10]
    target_ignore_limit = 0.02       # when target error < target_err_range*target_ignore_limit , set target error to 0
    pitch_reverse = False # reverse out value direction
    roll_reverse = True   # ..

    import sensor,image,lcd,gc
    import KPU as kpu
    from Maix import utils
    gc.collect()
    utils.gc_heap_size(0x80000)
    kpu.memtest()
    class Target():
        def __init__(self, out_range=10, ignore_limit=0.02, hmirror=False, vflip=False, lcd_rotation=2, lcd_mirror=True):
            self.pitch = 0
            self.roll = 0
            self.out_range = out_range
            self.ignore = ignore_limit
            self.task_fd = kpu.load("/sd/yolov2.kmodel")   #加载模型
            with open("anchors.txt","r") as f:
                anchor_txt=f.read()
            L=[]
            for i in anchor_txt.split(","):
                L.append(float(i))
            anchor=tuple(L)                    #物品名称
            f.close()
            kpu.init_yolo2(self.task_fd, 0.5, 0.3, 5, anchor)
            lcd.init()
            lcd.rotation(lcd_rotation)
            lcd.mirror(lcd_mirror)
            sensor.reset()
            sensor.set_pixformat(sensor.RGB565)
            sensor.set_framesize(sensor.QVGA)
            sensor.set_hmirror(1)
            sensor.set_vflip(0)
        def get_target_err(self):
            img = sensor.snapshot()
            img2=image.Image(copy_to_fb=True)
            img2=img.copy((48,8,224, 224))
            img2.pix_to_ai()
            code = kpu.run_yolo2(self.task_fd, img2)
            if code:
                max_area = 0
                max_i = 0
                for i, j in enumerate(code):
                    a = j.w()*j.h()
                    if a > max_area:
                        max_i = i
                        max_area = a

                warning.warning(0)
                img2 = img2.draw_rectangle(code[max_i].rect())

                self.pitch = (code[max_i].y() + code[max_i].h() / 2)/224*self.out_range*2 - self.out_range
                self.roll = (code[max_i].x() + code[max_i].w() / 2)/224*self.out_range*2 - self.out_range
                # limit
                if abs(self.pitch) < self.out_range*self.ignore:
                    self.pitch = 0
                if abs(self.roll) < self.out_range*self.ignore:
                    self.roll = 0
                img2 = img2.draw_cross(112, 112)
                lcd.display(img2)
                return (self.pitch, self.roll)
            else:
                img2 = img2.draw_cross(112, 112)
                lcd.display(img2)
                warning.warning(1)
                return (0, 0)


    target = Target(target_err_range, target_ignore_limit, sensor_hmirror, sensor_vflip, lcd_rotation, lcd_mirror)

    tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
    tim1 = Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM)
    pitch_pwm = PWM(tim0, freq=50, duty=0, pin=10)
    roll_pwm  = PWM(tim1, freq=50, duty=0, pin=11)
    pitch = Servo(pitch_pwm, dir=init_pitch)
    roll = Servo(roll_pwm, dir=init_roll)
    pid_pitch = PID(p=pitch_pid[0], i=pitch_pid[1], d=pitch_pid[2], imax=pitch_pid[3])
    pid_roll = PID(p=roll_pid[0], i=roll_pid[1], d=roll_pid[2], imax=roll_pid[3])
    gimbal = Gimbal(pitch, pid_pitch, roll, pid_roll)
    warning=WARNING(IO=14)
    target_pitch = init_pitch
    target_roll = init_roll
    t = time.ticks_ms()
    _dir = 0
    t0 = time.ticks_ms()
    while 1:
        # get target error
        err_pitch, err_roll = target.get_target_err()
        # interval limit to > 10ms
        if time.ticks_ms() - t0 < 10:
            continue
        t0 = time.ticks_ms()
        # run
        gimbal.run(err_pitch, err_roll, pitch_reverse = pitch_reverse, roll_reverse=roll_reverse)

