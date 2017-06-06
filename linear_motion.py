################################################################################################
#							  				       #
#     linear motion                                                                #
#       Xiang Zhai,   May 2, 2013                         				       #
#       zxzhaixiang at gmail.com							       #
#  For instruction on how to build the laser engraver and operate the codes, please visit      #
#   funofdiy.blogspot.com                                                                      #
#											       #
################################################################################################

import RPi.GPIO as GPIO
from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
import time
from numpy import pi, sin, cos, sqrt, arccos, arcsin

GPIO.setmode(GPIO.BOARD)
M=Bipolar_Stepper_Motor(11,7,5,3);       

speed=200;      #step/sec

try:
    for i in range(30):
    	print "Move to %s .." % ((i+1)*1000);
    	M.move(-1,1000,1.0/speed);
       
except KeyboardInterrupt:
    pass

M.unhold();

GPIO.cleanup();
