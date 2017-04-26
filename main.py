import network
import time
import arm 
import os
import PWM
import machine


Arm =arm.arm()
Arm.begin()

i2c = machine.I2C(scl=machine.Pin(12),sda=machine.Pin(14))
if i2c.scan==57:
	buff=bytearray(1)
	buff[0]=0
	i2c.writeto_mem(57,0x80,buff)
	buff[0]=219
	i2c.writeto_mem(57,0x81,buff)
	buff[0]=246
	i2c.writeto_mem(57,0x83,buff)
	buff[0]=0x60
	i2c.writeto_mem(57,0x8D,buff)
	buff[0]=1
	i2c.writeto_mem(57,0x8F,buff)
	buff[0]=3
	i2c.writeto_mem(57,0x80,buff)

def readcolor():
	color=bytearray(8)
	i2c.readfrom_mem_into(57,0x94,color)
	amb = color[0]+((int)(color[1])<<8)
	R = color[2]+((int)(color[3])<<8)
	G = color[4]+((int)(color[5])<<8)
	B = color[6]+((int)(color[7])<<8)
	print("amb: ",amb," R: ",R," G: ",G," B: ",B)