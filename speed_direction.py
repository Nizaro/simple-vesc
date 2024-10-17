import sys
from time import sleep, time
from pyvesc.VESC import VESC
import numpy as np


class Speed_Angle_Control():

    def __init__(self, serial_port):
    
        self.serial_port = serial_port # connection on the computer
        self.motor = VESC(serial_port=serial_port) # acces to the motors
        self.speed = 0
        self.wheel_radius = 4  # cm , can be usefull for odometry (rpm to speed)
        
        
    def speed_control_lp(self, speed_command=0.05):

        k = 0.005 # lowpass filter constant 
        
        err = speed_command - self.speed
        while(np.abs(err) > 0.01):
            self.speed += k*err
            self.speed = np.clip(self.speed,  -1, 1) # validity interval : [-1, 1]
            self.motor.set_duty_cycle(self.speed)
            err = speed_command - self.speed
            sleep(0.001)
        
        if (speed_command == 0):
            self.motor.set_rpm(0)
        
                
    def speed_control(self, speed_input=0.05):  
        if (speed_input == 0):
            self.motor.set_rpm(0)
        else:
            self.speed = np.clip(speed_input, -1, 1) # validity interval : [-1, 1]
            self.motor.set_duty_cycle(self.speed)#self.speed)
        
    def lowpass(self, speed_command):
        k = 0.01 # lowpass filter constant 
        
        err = speed_command - self.speed
        if(np.abs(err) > 0.01):
            self.speed += k*err
            self.speed = np.clip(self.speed,  -1, 1) # validity interval : [-1, 1]
        else:
            self.speed = speed_command         
        return self.speed # remove this after
        
    def turn_wheels(self, angle: float):
        self.motor.set_servo(angle)
        #self.motor.stop_heartbeat()
    
    #angle from -30 to 30 degrees mapped into 0 to 1 values
    def turn(self, angle: float) -> bool:
        self.deg_angle = angle
        angle = angle + 30 # 0 to 60
        mapped_angle = (angle/60) # 0 to 1
        self.mapped_angle = np.clip(mapped_angle, 0, 1) # to ensure to stay in range 0 - 1
        self.turn_wheels(self.mapped_angle)
        self.deg_angle = angle
        return True
    
    def reload(self, serial_port=""):
        #reload the controller
        if serial_port != "":
            self.serial_port = serial_port
            self.motor = VESC(serial_port=serial_port)
        
    
    def stop_motor(self):
        #stop the controller
        self.motor.stop_heartbeat()

class Transition():
    speed = 0
    timing = 0
    angle = 0
   
def rectangle():
        V0= 0.04
        
        #turn
        turn = Transition()
        turn.speed, turn.timing, turn.angle = V0/3, 0.2, 20
        
        t1 = Transition()
        t1.speed, t1.timing, t1.angle = V0, 3, 0
        
        t2 = Transition()
        t2.speed, t2.timing, t2.angle = V0, 2, 0
        
        t3 = Transition()
        t3.speed, t3.timing, t3.angle = V0*2, 1.5, 0
        
        t4 = Transition()
        t4.speed, t4.timing, t4.angle = V0/2, 4, 0
        
        return (t1, turn, t2, turn, t3, turn, t4, turn)
        
if __name__ =="__main__":
    
    serial_port = "COM6"
    sac = Speed_Angle_Control(serial_port)
    sac.motor.stop_heartbeat()
    sleep(0.1)
    print("Firmware: ", sac.motor.get_firmware_version())
    sleep(0.1)
    print(f"measurements = {dir(sac.motor.get_measurements())}")
    
    
    transitions = rectangle()
    
    for trans in transitions:
        time_init = time()
        time_end = time_init
        while((time_end -time_init) <trans.timing):
            print(trans.speed,trans.timing, trans.angle)
            
            vitesse = sac.lowpass(trans.speed)
            sac.speed_control(vitesse) 
            sleep(0.001)
            sac.turn(trans.angle)
            sleep(0.001)
            time_end = time()
        
    #stop the car
    sac.turn(0)
    sac.speed_control_lp(0)
    sleep(2)
    print("speed 0")
    sac.stop_motor()
    
    
    
        