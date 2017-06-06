################################################################################################
#							  				       #
#     Gray scale image engraving for 2D CNC laser engraver using Raspberry Pi                  #
#       Xiang Zhai,   Mar 12, 2015                         				       #
#       zxzhaixiang at gmail.com							       #
#  For instruction on how to build the laser engraver and operate the codes, please visit      #
#   funofdiy.blogspot.com                                                                      #
#											       #
################################################################################################

import RPi.GPIO as GPIO
import Motor_control
from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
import time
import Image

################################################################################################
################################################################################################
#################                            ###################################################
#################    Parameters set up       ###################################################
#################                            ###################################################
################################################################################################
################################################################################################

filename='plasma.jpg'; #file name of image

GPIO.setmode(GPIO.BOARD)

MX = Bipolar_Stepper_Motor(23,22,24,26);     #pin number for a1,a2,b1,b2.  a1 and a2 form coil A; b1 and b2 form coil B

MY = Bipolar_Stepper_Motor(11,7,5,3);       

Laser_switch=15;

Depth = 1; #a normalized factor determines how dark a solid dot is. Depth = 1 means the laser will stop at one location for 1 second if the the pixel value is 1

################################################################################################
################################################################################################
#################                            ###################################################
#################    Other initialization    ###################################################
#################                            ###################################################
################################################################################################
################################################################################################
    
GPIO.setup(Laser_switch,GPIO.OUT);

GPIO.output(Laser_switch,False);

X = 0;
Y = 0;

try:
    im = Image.open(filename);
    xsize,ysize = im.size;
    
    im_data=im.load();
    
    print im.size,im.format,im.mode;

    for i in range(xsize):
        GPIO.output(Laser_switch,False);
        Motor_control.Motor_Step(MX,1,MY,0-Y,25);
        X = X + 1;
        Y = 0;
        
        for j in range(ysize):
            brightness = sum(im_data[i,ysize-j-1])/255.0/3.0;
            dt = brightness * depth;

            Motor_control.Motor_Step(MX,0,MY,1,25);
            Y = Y + 1;
            
            if dt>0.01:
                GPIO.output(Laser_switch,True);
                sleep(dt);

            GPIO.output(Laser_swith,False);
        
except KeyboardInterrupt:
    pass


GPIO.output(Laser_switch,False);   # turn off laser
Motor_control.Motor_Step(MX,-X,MY,-Y,25);

MX.unhold();
MY.unhold();

GPIO.cleanup();
