from vedder_config import config, message2bytes
    
if __name__ == "__main__":

    messages = config()
    
    #control duty cycle
    messages["duty_cycle"].value = 0.001
    print(messages["duty_cycle"].value)
    message2bytes(messages["duty_cycle"])
    
    #control servo moteur
    messages["servo_pos"].value = 0.007
    print(messages["servo_pos"].value)
    message2bytes(messages["servo_pos"])

    #alive heartbeat
    print(messages["alive"].value)
    message2bytes(messages["alive"])
    