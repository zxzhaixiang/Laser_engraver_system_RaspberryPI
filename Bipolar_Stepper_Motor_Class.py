import RPi.GPIO as GPIO
import time

# sequence for a1, b2, a2, b1
# phase_seq=[[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]]
# full step sequence. maximum torque
phase_seq = [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [
    0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]]
# half-step sequence. double resolution. But the torque of the stepper motor is not constant
num_phase = len(phase_seq)


class Bipolar_Stepper_Motor:

    phase = 0
    dir = 0
    position = 0

    def __init__(self, a1, a2, b1, b2, axis='X'):
        # initial a Bipolar_Stepper_Moter objects by assigning the pins
        GPIO.setmode(GPIO.BOARD)

        self.axis = axis
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2

        GPIO.setup(self.a1, GPIO.OUT)
        GPIO.setup(self.a2, GPIO.OUT)
        GPIO.setup(self.b1, GPIO.OUT)
        GPIO.setup(self.b2, GPIO.OUT)

        self.phase = 0
        self.dir = 0
        self.position = 0

    def move(self, dir, steps):
        multiplier = 1

        # to make bottom left as home position
        if(self.axis == 'X'):
            multiplier = -1

        for _ in range(steps):
            next_phase = (self.phase+(multiplier * dir)) % num_phase

            GPIO.output(self.a1, phase_seq[next_phase][0])
            GPIO.output(self.b2, phase_seq[next_phase][1])
            GPIO.output(self.a2, phase_seq[next_phase][2])
            GPIO.output(self.b1, phase_seq[next_phase][3])

            self.phase = next_phase
            self.dir = dir
            self.position += dir

            time.sleep(0.03)

    def unhold(self):
        GPIO.output(self.a1, 0)
        GPIO.output(self.a2, 0)
        GPIO.output(self.b1, 0)
        GPIO.output(self.b2, 0)
