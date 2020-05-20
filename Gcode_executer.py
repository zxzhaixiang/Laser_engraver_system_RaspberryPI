################################################################################################
#                                                                                              #
#     G code interpreter and executer for 2D CNC engraver using Raspberry Pi                   #
#       Xiang Zhai,   Oct 1, 2013                         	                                   #
#       zxzhaixiang at gmail.com                                                               #
#  For instruction on how to build the engraver and operate the codes, please visit            #
#   funofdiy.blogspot.com                                                                      #
#                                                                                              #
################################################################################################

import RPi.GPIO as GPIO
import Motor_control
from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
import time
from math import pi, sin, cos, sqrt, acos, asin
import sys

################################################################################################
################################################################################################
#################                            ###################################################
#################    Parameters set up       ###################################################
#################                            ###################################################
################################################################################################
################################################################################################

filename = 'Tsinghua_symbol.nc'  # file name of the G code commands

if len(sys.argv) > 1:
    filename = str(sys.argv[1])

GPIO.setmode(GPIO.BOARD)

# pin number for a1,a2,b1,b2.  a1 and a2 form coil A b1 and b2 form coil B
MX = Bipolar_Stepper_Motor(11, 12, 15, 13, 'X')

MY = Bipolar_Stepper_Motor(16, 18, 37, 36, 'Y')

Pen_switch = 32

dx = 0.075  # resolution in x direction. Unit: mm
dy = 0.075  # resolution in y direction. Unit: mm
IsPenDown = 2  # 0 - false, 1 - true 2 - unknown

#######B#########################################################################################
################################################################################################
#################                            ###################################################
#################    Other initialization    ###################################################
#################                            ###################################################
################################################################################################
################################################################################################

GPIO.setup(Pen_switch, GPIO.OUT)
MZ = GPIO.PWM(Pen_switch, 50)
MZ.start(0)


def SetPenDown(isdown):
    global IsPenDown

    if(isdown == True and IsPenDown != 1):
        print('Pen Down')
        MZ.ChangeDutyCycle(2+(90/18))
        time.sleep(0.5)
        MZ.ChangeDutyCycle(0)
        IsPenDown = 1

    if(isdown == False and IsPenDown != 0):
        print('Pen UP')
        MZ.ChangeDutyCycle(2+(130/18))
        time.sleep(0.7)
        MZ.ChangeDutyCycle(0)
        IsPenDown = 0

################################################################################################
################################################################################################
#################                                ###############################################
#################    G code reading Functions    ###############################################
#################                                ###############################################
################################################################################################
################################################################################################


def XYposition(lines):
    # given a movement command line, return the X Y position
    xchar_loc = lines.index('X')
    i = xchar_loc+1
    while (47 < ord(lines[i]) < 58) | (lines[i] == '.') | (lines[i] == '-'):
        i += 1
    x_pos = float(lines[xchar_loc+1:i])

    ychar_loc = lines.index('Y')
    i = ychar_loc+1
    while (47 < ord(lines[i]) < 58) | (lines[i] == '.') | (lines[i] == '-'):
        i += 1
    y_pos = float(lines[ychar_loc+1:i])

    return x_pos, y_pos


def IJposition(lines):
    # given a G02 or G03 movement command line, return the I J position
    ichar_loc = lines.index('I')
    i = ichar_loc+1
    while (47 < ord(lines[i]) < 58) | (lines[i] == '.') | (lines[i] == '-'):
        i += 1
    i_pos = float(lines[ichar_loc+1:i])

    jchar_loc = lines.index('J')
    i = jchar_loc+1
    while (47 < ord(lines[i]) < 58) | (lines[i] == '.') | (lines[i] == '-'):
        i += 1
    j_pos = float(lines[jchar_loc+1:i])

    return i_pos, j_pos


def moveto(MX, x_pos, dx, MY, y_pos, dy):
    # Move to (x_pos,y_pos) (in real unit)
    stepx = int(round(x_pos/dx))-MX.position
    stepy = int(round(y_pos/dy))-MY.position

    print('Movement: Dx=', stepx, '  Dy=', stepy)
    Motor_control.Motor_Step(MX, stepx, MY, stepy)

    return 0

###########################################################################################
###########################################################################################
#################                           ###############################################
#################    Main program           ###############################################
#################                           ###############################################
###########################################################################################
###########################################################################################


try:  # read and execute G code
    SetPenDown(False)
    for lines in open(filename, 'r'):
        print(lines)
        if lines == []:
            1  # blank lines

        elif lines[0:3] == 'G90':
            print('start')

        elif lines[0:3] == 'G20':  # working in inch
            dx /= 25.4
            dy /= 25.4
            print('Working in inch')

        elif lines[0:3] == 'G21':  # working in mm
            print('Working in mm')

        elif lines[0:3] == 'M05':
            SetPenDown(False)

        elif lines[0:3] == 'M03':
            SetPenDown(True)

        elif lines[0:3] == 'M02':
            SetPenDown(False)
            print('finished. shuting down')
            break

        elif (lines[0:3] == 'G1F') | (lines[0:4] == 'G1 F'):
            1  # do nothing

        elif (lines[0:5] == 'G01 Z'):
            SetPenDown(True)

        elif (lines[0:5] == 'G00 Z'):
            SetPenDown(False)

        # |(lines[0:3]=='G02')|(lines[0:3]=='G03'):
        elif (lines[0:3] == 'G0 ') | (lines[0:3] == 'G1 ') | (lines[0:3] == 'G00') | (lines[0:3] == 'G01'):
            # linear engraving movement
            if (lines[0:3] == 'G0 ' or lines[0:3] == 'G00'):
                engraving = False
            else:
                engraving = True

            SetPenDown(engraving)

            if (lines.find('X') != -1 and lines.find('Y') != -1):
                [x_pos, y_pos] = XYposition(lines)
                moveto(MX, x_pos, dx, MY, y_pos, dy)

        elif (lines[0:3] == 'G02') | (lines[0:3] == 'G03'):  # circular interpolation
            if (lines.find('X') != -1 and lines.find('Y') != -1 and lines.find('I') != -1 and lines.find('J') != -1):
                SetPenDown(True)

                old_x_pos = x_pos
                old_y_pos = y_pos

                [x_pos, y_pos] = XYposition(lines)
                [i_pos, j_pos] = IJposition(lines)

                xcenter = old_x_pos+i_pos  # center of the circle for interpolation
                ycenter = old_y_pos+j_pos

                Dx = x_pos-xcenter
                # vector [Dx,Dy] points from the circle center to the new position
                Dy = y_pos-ycenter

                r = sqrt(i_pos**2+j_pos**2)   # radius of the circle

                # pointing from center to current position
                e1 = [-i_pos, -j_pos]
                if (lines[0:3] == 'G02'):  # clockwise
                    # perpendicular to e1. e2 and e1 forms x-y system (clockwise)
                    e2 = [e1[1], -e1[0]]
                else:  # counterclockwise
                    # perpendicular to e1. e1 and e2 forms x-y system (counterclockwise)
                    e2 = [-e1[1], e1[0]]

                # [Dx,Dy]=e1*cos(theta)+e2*sin(theta), theta is the open angle

                costheta = (Dx*e1[0]+Dy*e1[1])/r**2
                # theta is the angule spanned by the circular interpolation curve
                sintheta = (Dx*e2[0]+Dy*e2[1])/r**2

                # there will always be some numerical errors! Make sure abs(costheta)<=1
                if costheta > 1:
                    costheta = 1
                elif costheta < -1:
                    costheta = -1

                theta = acos(costheta)
                if sintheta < 0:
                    theta = 2.0*pi-theta

                # number of point for the circular interpolation
                no_step = int(round(r*theta/dx/5.0))

                for i in range(1, no_step+1):
                    tmp_theta = i*theta/no_step
                    tmp_x_pos = xcenter+e1[0] * \
                        cos(tmp_theta)+e2[0]*sin(tmp_theta)
                    tmp_y_pos = ycenter+e1[1] * \
                        cos(tmp_theta)+e2[1]*sin(tmp_theta)
                    moveto(MX, tmp_x_pos, dx, MY, tmp_y_pos, dy)

except KeyboardInterrupt:
    pass

SetPenDown(False)   # up the pen
moveto(MX, 0, dx, MY, 0, dy)  # move back to Origin

MZ.stop()
MX.unhold()
MY.unhold()

GPIO.cleanup()
