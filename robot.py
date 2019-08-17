import RPi.GPIO as GPIO
import smbus
import time
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)
GPIO.setwarnings(False)
pwm = GPIO.PWM(18, 100)

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
   	return bus.read_byte_data(address, adr)

def read_word(adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
	val = (high << 8) + low
	return val

def read_word_2c(adr):
	val = read_word(adr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

def dist(a,b):
	return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians)

def servo_val(angle):
    return angle/-10+11.5

bus = smbus.SMBus(1)
address = 0x68
bus.write_byte_data(address, power_mgmt_1, 0)

pwm.start(servo_val(0))
for x in range(0,28):
	acc_x = read_word_2c(0x3b) / 16384.0
	acc_y = read_word_2c(0x3d) / 16384.0
	acc_z = read_word_2c(0x3f) / 16384.0
	x_rot = -get_x_rotation(acc_x, acc_y, acc_z)
	if x_rot < -0:
		pwm.ChangeDutyCycle(servo_val(13))
	elif x_rot > 0:
		pwm.ChangeDutyCycle(servo_val(-45))
	
	time.sleep(1.1)
pwm.stop()



