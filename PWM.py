import machine

class PWM :
	def __init__(self,debug=False):
		self.D1=machine.Pin(5)
		self.D2=machine.Pin(4)
		self.D3=machine.Pin(0)
		self.D4=machine.Pin(2)
		self.pwm1 = machine.PWM(self.D1)
		self.pwm2 = machine.PWM(self.D2)
		self.pwm3 = machine.PWM(self.D3)
		self.pwm4 = machine.PWM(self.D4)
	def setPWMFreq(self,freq):
		self.pwm1.freq(freq)
		self.pwm2.freq(freq)
		self.pwm3.freq(freq)
		self.pwm4.freq(freq)
	def setPWM(self,channel,duty):
		if channel==1:
			self.pwm1.duty(duty)
		elif channel==2:
			self.pwm2.duty(duty)
		elif channel==3:
			self.pwm3.duty(duty)
		elif channel==4:
			self.pwm4.duty(duty)