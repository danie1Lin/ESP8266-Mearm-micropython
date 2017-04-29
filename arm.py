import kinematics
import time
from math import pi
import PWM

class arm():
    def __init__(self, sweepMinBase = 118, sweepMaxBase = 35, angleMinBase = -pi/2, angleMaxBase = pi/2,
             sweepMinShoulder = 120, sweepMaxShoulder = 75, angleMinShoulder = 0, angleMaxShoulder = pi/2,
             sweepMinElbow = 83, sweepMaxElbow = 30, angleMinElbow = 0, angleMaxElbow = pi/2,
             sweepMinGripper = 50, sweepMaxGripper = 100, angleMinGripper = pi/2, angleMaxGripper = 0):
        """Constructor for meArm - can use as default arm=meArm(), or supply calibration data for servos."""
        self.servoInfo = {}
        self.servoInfo["base"] = self.setupServo(sweepMinBase, sweepMaxBase, angleMinBase, angleMaxBase)
        self.servoInfo["shoulder"] = self.setupServo(sweepMinShoulder, sweepMaxShoulder, angleMinShoulder, angleMaxShoulder)
        self.servoInfo["elbow"] = self.setupServo(sweepMinElbow, sweepMaxElbow, angleMinElbow, angleMaxElbow)
        self.servoInfo["gripper"] = self.setupServo(sweepMinGripper, sweepMaxGripper, angleMinGripper, angleMaxGripper)
        self.angles=[0,0,0]
        self.pwmValue=[0,0,0]
    # Adafruit servo driver has four 'blocks' of four servo connectors, 0, 1, 2 or 3.
    def begin(self):
        """Call begin() before any other meArm calls.  Optional parameters to select a different block of servo connectors or different I2C address."""
        self.pwm = PWM.PWM() # Address of Adafruit PWM servo driver
        self.base = 1
        self.shoulder = 2
        self.elbow = 3
        self.gripper = 4
        self.pwm.setPWMFreq(50)
        self.openGripper()
        self.goDirectlyTo(0, 100, 50)
    def setupServo(self, n_min, n_max, a_min, a_max):
        """Calculate servo calibration record to place in self.servoInfo"""
        rec = {}
        n_range = n_max - n_min
        a_range = a_max - a_min
        if a_range == 0: return
        gain = n_range / a_range
        zero = n_min - gain * a_min
        rec["gain"] = gain
        rec["zero"] = zero
        rec["min"] = n_min
        rec["max"] = n_max
        return rec
    
    def angle2pwm(self, servo, angle):
        """Work out pulse length to use to achieve a given requested angle taking into account stored calibration data"""
        ret =int(self.servoInfo[servo]["zero"] + self.servoInfo[servo]["gain"] * angle)
        print(servo,ret)
        return ret

    def goDirectlyTo(self, x, y, z):
        if kinematics.solve(x, y, z, self.angles):
            radBase = self.angles[0]
            radShoulder = self.angles[1]
            radElbow = self.angles[2]
            self.pwm.setPWM(self.base, self.angle2pwm("base", radBase))
            self.pwm.setPWM(self.shoulder, self.angle2pwm("shoulder", radShoulder))
            self.pwm.setPWM(self.elbow, self.angle2pwm("elbow", radElbow))
            self.x = x
            self.y = y
            self.z = z

    def gotoPoint(self, x, y, z):
        """Travel in a straight line from current position to a requested position"""
        x0 = self.x
        y0 = self.y
        z0 = self.z
        dist = kinematics.distance(x0, y0, z0, x, y, z)
        step = 10
        i = 0
        while i < dist:
            self.goDirectlyTo(x0 + (x - x0) * i / dist, y0 + (y - y0) * i / dist, z0 + (z - z0) * i / dist)
            time.sleep(0.05)
            i += step
        self.goDirectlyTo(x, y, z)
        time.sleep(0.05)

    def openGripper(self):
        """Open the gripper, dropping whatever is being carried"""
        self.pwm.setPWM(self.gripper, self.angle2pwm("gripper", pi/2))
        time.sleep(0.3)
    	
    def closeGripper(self):
        """Close the gripper, grabbing onto anything that might be there"""
        self.pwm.setPWM(self.gripper,self.angle2pwm("gripper", 0))
        time.sleep(0.3)
    
    def isReachable(self, x, y, z):
        """Returns True if the point is (theoretically) reachable by the gripper"""
        radBase = 0
        radShoulder = 0
        radElbow = 0
        return kinematics.solve(x, y, z,[radBase, radShoulder, radElbow])
    
    def getPos(self):
        """Returns the current position of the gripper"""
        return [self.x, self.y, self.z]
    def checkRest(self):
        angles=[0,0,0]
        [x,y,z]=self.getPos()
        kinematics.solve(x,y,z,angles)
        for a in range(0,3):
            if angles[a]==self.angles[a]:
                self.pwm.setPWM(a+1,0)
                print(a,"is rest")
        self.angles=angles
    def relative(self,x,y,z):
        [x0,y0,z0]=self.getPos()
        x0=x0+x
        y0=y0+y
        z0=z0+z

        if kinematics.solve(x0, y0, z0, self.angles):
            radBase = self.angles[0]
            radShoulder = self.angles[1]
            radElbow = self.angles[2]
            self.pwm.setPWM(self.base, self.angle2pwm("base", radBase))
            self.pwm.setPWM(self.shoulder, self.angle2pwm("shoulder", radShoulder))
            self.pwm.setPWM(self.elbow, self.angle2pwm("elbow", radElbow))
            self.x = x0
            self.y = y0
            self.z = z0
    def gotoAngle(self,a1,a2,a3):
        self.pwm.setPWM(self.base, self.angle2pwm("base", a1*pi/180))
        self.pwm.setPWM(self.shoulder, self.angle2pwm("shoulder", a2*pi/180))
        self.pwm.setPWM(self.elbow, self.angle2pwm("elbow", a3*pi/180))
        [self.x,self.y,self.z]=kinematics.unsolve(a1,a2,a3)
        print(self.angles)