import sys
import time
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
            self.speed = np.clip(self.speed,  -1, 1) # validity interval : [-1e5, 1e5]
            self.motor.set_duty_cycle(self.speed)
            err = speed_command - self.speed
            time.sleep(0.05)
        
        if (speed_command == 0):
            self.motor.set_rpm(0)
        
                
    def speed_control(self, speed_command=0.05):
        
        if (speed_command == 0):
            self.motor.set_rpm(0)
        else:
            
            self.speed = np.clip(speed_command, -1, 1) # validity interval : [-1e5, 1e5]
            print(self.speed, speed_command)
            self.motor.set_duty_cycle(.02)#self.speed)
        
        
                
    def turn_wheels(self, angle: float) -> bool:
        self.motor.set_servo(angle)
        self.motor.stop_heartbeat()
    
    #angle from -30 to 30 degrees mapped into 0 to 1 values
    def turn(self, angle: float) -> bool:
        self.deg_angle = angle
        angle = angle + 30 # 0 to 60
        mapped_angle = (angle/60) # 0 to 1
        self.mapped_angle = np.clip(mapped_angle, 0, 1) # to ensure to stay in range 0 - 100
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
        
        
if __name__ =="__main__":
    
    serial_port = "COM6"
    sac = Speed_Angle_Control(serial_port)
    sac.motor.stop_heartbeat()
    time.sleep(0.1)
    print("Firmware: ", sac.motor.get_firmware_version())
    time.sleep(0.1)
    print(f"measurements = {dir(sac.motor.get_measurements())}")
    time.sleep(3)
    sac.speed_control_lp(0.05) 
    sac.turn(10)
    time.sleep(1)
    time.sleep(1)
    sac.speed_control_lp(-0.05)
    time.sleep(1)
    sac.turn(10)
    time.sleep(1)
    
    sac.turn(10)
    time.sleep(1)
    sac.turn(-10)
    time.sleep(1)
    
    
    
    #stop the car
    sac.speed_control_lp(0)
    time.sleep(2)
    print("speed 0")
    sac.stop_motor()
    
    
        