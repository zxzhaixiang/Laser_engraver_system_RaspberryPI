# Raspberry Pi based Laser Engraver System

This package includes python class and scripts for Raspberry Pi to control a home-made mini CNC laser engraver.

For detailed instruction on how to build and set up the laser engraver, please visit my blog

http://funofdiy.blogspot.com/2013/10/a-raspberry-pi-controlled-mini-laser.html

Check my other post as well
funofdiy.blogspot.com



########################################################################################################

## Gcode_executer.py
This is the main program. You need to modify line 25 (G code file name), line 29 (pin numbers 
for stepper motor X), line 31 (pin numbers for stepper motor Y), line 32 (pin number for laser 
switch), line 35, 36 (resolution of the machine in unit of mm/step) and line 38 (engraving speed).
The code read and interpret G code, and send corresponding commands to the motor control functions.

Currently, the Gcdoe_executer.py only accepts limited number of G commands: G90, G20, G21, M05, M03, M02, G01,  G02, G03.
The code can recognize G1F commands (engraving speed) but simply ignore it.  Engraving speed is set by line 38 in unit of mm/sec.

## Bipolar_Stepper_Motor_Class.py
defines the Bipolar_Stepper_Motor class. By default, line 5 is commented and line 7 is valid. 
This corresponds to a 8-step half-angle sequence. If maximum torque is desired, you can comment 
line 7 and uncomment line 5 to select 4-step full-angle sequence.

## Motor_control.py
defines a set of functions such as LCM (for calculating the lcm of two integers) and Motor_Step 
(for controlling two motors simultaneously). Usually you don't need to modify anything.

## spiral.nc
This is a simple G code which plots a small spiral. It can perfectly test whether the machine 
can process G code, especially the circular interpolation G02 and G03, correctly.

## grid.nc
A simple G code which plots several straight lines to make a grid. Perfect code to test the 
machine and make a coordinate system!

########################################################################################################

As mentioned at the beginning of this post, D. Miller made some improvement to my code so that the code 
can work along with the inkscape GCodeTools extension and allow remote engraving via another small python 
script he wrote. The modified version can be downloaded here https://github.com/iandouglas96/engravR
