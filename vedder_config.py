from crccheck.crc import CrcXmodem
from vedder_definitions import VedderFct, VedderType, VedderMessage

def config_cmd(messages, name, fct, type_, scale):
    # config
    vm = VedderMessage()
    vm.name = name # "duty_cycle"
    vm.fct = fct # vf.COMM_SET_DUTY
    vm.type = type_# vt.int
    vm.scale = scale # 100000

    # define value
    vm.value = -1 # before initialisation

    messages[vm.name] = vm # add a new command in message

def message2bytes(message):
    begin = b'\x02'
    end = b'\x03'
    
    cmd_size = message.type+1 # size of the value + 1 byte for fct
    cmd_size = cmd_size.to_bytes(1, byteorder='big') 
    
    fct = message.fct
    fct = fct.to_bytes(1, byteorder='big')  
    
    if message.type > 0:
        value = int(message.value*message.scale)
        value = value.to_bytes(message.type, byteorder='big')  
        #print(value)
    else:
        value = b''
    
    cmd = fct + value
    
    
    check_val = check_bytes(cmd) # hexa string '0x586'
    check_val = int(check_val, 16) # integer 1414
    check_val = check_val.to_bytes(2, byteorder='big')
    

    print(begin + cmd_size + cmd + check_val + end)
    #else:
    #    print(begin + cmd_size + cmd + end)
    return begin + cmd_size + cmd + check_val + end
    

crc_checker = CrcXmodem()

def check_bytes(data):
    #data = b'\x0c\x00\x07'
    val = crc_checker.calc(data)
    return hex(val)
    
    
def config():

    # configuration
    vt = VedderType()
    vf = VedderFct()

    messages = {}

    #duty cycle
    config_cmd(messages, name = "duty_cycle", fct= vf.COMM_SET_DUTY, 
           type_ = vt.int, scale = 100000)
    #duty cycle
    config_cmd(messages, name = "servo_pos", fct= vf.COMM_SET_SERVO_POS, 
           type_ = vt.short, scale = 1000)
    #heartbeat alive       
    config_cmd(messages, name = "alive", fct= vf.COMM_ALIVE, 
           type_ = vt.null, scale = -1)
           
    return messages