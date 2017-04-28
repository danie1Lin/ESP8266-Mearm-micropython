#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DemoIK.py - York Hack Space May 2014
#  Simple demo of meArm library to walk through some points defined in Cartesian coordinates

import meArm
addr = 0x39
GDATAH = 0x96
GDATAL = 0x97
BDATAH = 0x98
BDATAL = 0x99
RATAH = 0x9A
RDATAL = 0x9B
ENABLE = 
ALL=0x7F
def main():
    arm = meArm.meArm()
    arm.begin()
	
    while True:
        arm.openGripper()
        arm.closeGripper()
        arm.openGripper()
        arm.closeGripper()
        arm.openGripper()

        arm.gotoPoint(0, 150, 50)
        arm.gotoPoint(0, 150, 0)
        arm.gotoPoint(0, 150, 150)
        arm.gotoPoint(0, 150, 50)
        arm.gotoPoint(-150, 150, 50)
        arm.gotoPoint(150, 150, 50)
        arm.gotoPoint(0, 150, 50)
        arm.gotoPoint(0, 100, 50)

if __name__ == '__main__':
    main()
