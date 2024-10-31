from microbit import sleep, i2c, pin0, pin1, pin2, pin12, pin15, pin16
from machine import time_pulse_us
import utime

MICROBIT_CAR_ADDR = 0x11

# Registers
RGB_LIGHT_ALL = 0x01
RGB_LIGHT_LEFT = 0x0B
RGB_LIGHT_RIGHT = 0x0C
BUZZER_STATE = 0x02
BUZZER_SOUND = 0x03
CAR_STATE = 0x04
MOTOR_SPEED = 0x05
SERVO_STATE = 0x06
NEOPIXEL_ALL = 0x07
NEOPIXEL_ALONE = 0x08

class Led:
    COLOR_RGB = {
        'RED': 0,
        'GREEN': 1,
        'BLUE': 2,
        'YELLOW': 3,
        'ORANGE': 4,
        'PURPLE': 5,
        'LAKE': 6,
        'WHITE': 7,
        'OFF': 8
    }

    def rgb_led_all(self, color_name: str):
        buf = bytearray(2)
        buf[0] = RGB_LIGHT_ALL
        buf[1] = self.COLOR_RGB[color_name]  # 딕셔너리에서 값 가져오기
        i2c.write(MICROBIT_CAR_ADDR, buf)

    def rgb_led_left(self, color_name: str):
        buf = bytearray(2)
        buf[0] = RGB_LIGHT_LEFT
        buf[1] = self.COLOR_RGB[color_name]  # 딕셔너리에서 값 가져오기
        i2c.write(MICROBIT_CAR_ADDR, buf)

    def rgb_led_right(self, color_name: str):
        buf = bytearray(2)
        buf[0] = RGB_LIGHT_RIGHT
        buf[1] = self.COLOR_RGB[color_name]  # 딕셔너리에서 값 가져오기
        i2c.write(MICROBIT_CAR_ADDR, buf)

class Buzzer:

    SOUND_LEV = {
        'LEVEL_1': 0x02,
        'LEVEL_2': 0x04,
        'LEVEL_3': 0x06
    }

    # BEEP음 OFF
    def beep_off(self):
        buf = bytearray(2)
        buf[0] = BUZZER_STATE
        buf[1] = 0x00
        i2c.write(MICROBIT_CAR_ADDR, buf)

    # BEEP음 울림
    def beep_sound(self, timbre: int, duration: int, sound_level: str):
        # Timbre 범위 제한
        timbre = max(0, min(timbre, 1000))

        buf = bytearray(4)
        buf[0] = BUZZER_SOUND
        buf[1] = (timbre >> 8) & 0x0F
        buf[2] = timbre & 0xFF
        buf[3] = self.SOUND_LEV[sound_level]
        i2c.write(MICROBIT_CAR_ADDR, buf)

        # 지정된 시간 동안 대기 (밀리초)
        sleep(duration)

        # BEEP_OFF 함수 호출
        self.beep_off()
    
class Servo:
    SERVO_ID_PWM = {
        'SERVO_S1' : 0,
        'SERVO_S2' : 1,
        'SERVO_S3' : 2,
        'SERVO_S4' : 3,
    }

    # SERVO 모터 180도 제어
    def set_pwm_servo_180(self, servoID: str, angle: int):
        if (angle > 180):
            angle = 180
        elif (angle < 0):
            angle = 0

        buf = bytearray(3)
        buf[0] = SERVO_STATE
        buf[1] = self.SERVO_ID_PWM[servoID]
        buf[2] = angle

        i2c.write(MICROBIT_CAR_ADDR, buf)

    # SERVO 모터 270도 제어
    def set_pwm_servo_270(self, servoID: str, angle: int):
        if (angle > 270):
            angle = 270
        elif (angle < 0):
            angle = 0

        angle = angle / 270 * 180
        angle = round(angle)

        buf = bytearray(3)
        buf[0] = SERVO_STATE
        buf[1] = self.SERVO_ID_PWM[servoID]
        buf[2] = angle
        i2c.write(MICROBIT_CAR_ADDR, buf)

    # SERVO 모터 360도 제어
    def set_pwm_servo_360(self, servoID: str, angle: int):
        if (angle > 360):
            angle = 360
        elif (angle < 0):
            angle = 0

        angle = angle / 360 * 180
        angle = round(angle)

        buf = bytearray(3)
        buf[0] = SERVO_STATE
        buf[1] = self.SERVO_ID_PWM[servoID]
        buf[2] = angle
        i2c.write(MICROBIT_CAR_ADDR, buf)


class Gpio:
    PIN_GPIO = {
        'P0': 0,
        'P1': 1,
        'P2': 2,
        'P12': 12,
    }

    PIN_READ_MODE = {
        'Digital': 0,
        'Analog': 1,
    }

    # GPIO핀 디지털 출력 제어
    def gpio_output(self, GpioPin: str, value: int):
        if (self.PIN_GPIO[GpioPin] == 0):
            return pin0.write_digital(value)
        if (self.PIN_GPIO[GpioPin] == 1):
            return pin1.write_digital(value)
        if (self.PIN_GPIO[GpioPin] == 2):
            return pin2.write_digital(value)
        if (self.PIN_GPIO[GpioPin] == 12):
            return pin12.write_digital(value)

    def gpio_output_analog(self, GpioPin: str, value: int):
        if (self.PIN_GPIO[GpioPin] == 0):
            return pin0.write_analog(value)
        if (self.PIN_GPIO[GpioPin] == 1):
            return pin1.write_analog(value)
        if (self.PIN_GPIO[GpioPin] == 2):
            return pin2.write_analog(value)
        if (self.PIN_GPIO[GpioPin] == 12):
            return pin12.write_analog(value)

    def gpio_input(self, GpioPin: str, mode: int):
        if (mode == 'Digital'):
            if (self.PIN_GPIO[GpioPin] == 0):
                return pin0.read_digital()
            if (self.PIN_GPIO[GpioPin] == 1):
                return pin1.read_digital()
            if (self.PIN_GPIO[GpioPin] == 2):
                return pin2.read_digital()
            if (self.PIN_GPIO[GpioPin] == 12):
                return pin12.read_digital()
        elif (mode == 'Analog'):
            if (self.PIN_GPIO[GpioPin] == 0):
                return pin0.read_analog()
            if (self.PIN_GPIO[GpioPin] == 1):
                return pin1.read_analog()
            if (self.PIN_GPIO[GpioPin] == 2):
                return pin2.read_analog()
            if (self.PIN_GPIO[GpioPin] == 12):
                return pin12.read_analog()

        return 0

class NeoPixel:
    NEOPIXEL_COLOR = {
        'RED': 0,
        'GREEN': 1,
        'BLUE': 2,
        'YELLOW': 3,
        'PURPLE': 4,
        'ORANGE': 5,
        'INDIGO': 6,
        'WHITE': 7,
        'OFF': 8,
    }

    NEOPIXEL_STATE = {
        'OFF': 0,
        'ON': 1,
    }

    def set_neo_all(self, value: str, color: str):
        buf = bytearray(3)
        buf[0] = NEOPIXEL_ALL
        buf[1] = self.NEOPIXEL_STATE[value]
        buf[2] = self.NEOPIXEL_COLOR[color]
        i2c.write(MICROBIT_CAR_ADDR, buf)

    def set_neo_index(self, index: int, value: str, color: str):
        if index > 3:
            index = 3
        elif index < 0 :
            index = 0
        buf = bytearray(4)
        buf[0] = NEOPIXEL_ALONE
        buf[1] = index
        buf[2] = self.NEOPIXEL_STATE[value]
        buf[3] = self.NEOPIXEL_COLOR[color]
        i2c.write(MICROBIT_CAR_ADDR, buf)

class UltraSonic:
    def sonic(self):
        distances = []

        for i in range(5):

            pin15.write_digital(0)
            utime.sleep_us(2)
            pin15.write_digital(1)
            utime.sleep_us(15)
            pin15.write_digital(0)

            d = time_pulse_us(pin16, 1, 43200)
            distances.append(d // 40)

        distances.sort()
        length = (distances[1] + distances[2] + distances[3]) // 3
        return length

class Motor:
    MOTOR_STATE = {
        'STOP' : 0,
        'RUN' : 1,
        'BACK' : 2,
        'LEFT' : 3,
        'RIGHT' : 4,
        'LEFT_SPIN' : 5,
        'RIGHT_SPIN' : 6
    }

    def move(self, state: str, speed: int):
        if speed < 0:
            speed = 0
        elif speed > 1000:
            speed = 1000

        buf = bytearray(4)
        buf[0] = CAR_STATE
        buf[1] = self.MOTOR_STATE[state]
        buf[2] = (speed >> 8) & 0x0F
        buf[3] = speed & 0xFF
        i2c.write(MICROBIT_CAR_ADDR, buf)

    def stop(self):
        buf = bytearray(2)
        buf[0] = CAR_STATE
        buf[1] = self.MOTOR_STATE['STOP']
        i2c.write(MICROBIT_CAR_ADDR, buf)

    def abs(self, number: int):
        if (number < 0):
            return -number
        return number

    def move_motor(self, speed_L: int, speed_R: int):
        if speed_L > 1000:
            speed_L = 1000
        elif speed_L < -1000:
            speed_L = -1000

        if speed_R > 1000:
            speed_R = 1000
        elif speed_R < -1000:
            speed_R = -1000

        speed_L_send = self.abs(speed_L)
        speed_R_send = self.abs(speed_R)

        buf = bytearray(7)
        buf[0] = MOTOR_SPEED

        if (speed_L < 0):
            buf[3] = 1
        else:
            buf[3] = 0

        if (speed_L < 0):
            buf[6] = 1
        else:
            buf[6] = 0

        buf[1] = (speed_L_send >> 8) & 0x00FF
        buf[2] = speed_L_send & 0x00FF

        buf[4] = (speed_R_send >> 8) & 0x00FF
        buf[5] = speed_R_send & 0x00FF

        i2c.write(MICROBIT_CAR_ADDR, buf)

# 인스턴스 생성

# while True: