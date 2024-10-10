# simple-vesc

Simple Vesc is a librairy aiming to simplify the usage of Vedder's Vesc command.

## command format
The general command format is:  
begin + cmd_size + cmd + check_val + end  
with : 
### The bytes for begin and end :
  begin = b'\x02'  
  end = b'\x03'
### The size of the command (cmd_size)
  cmd_size = N data bytes + 1 fonction byte  
  example: b'\x03'
### Command (cmd)
  cmd = 1 byte fct + N bytes data  
  example: b'\x0c\x00\x07'  
  fct= 12 and size of the data is N=2, the value the data is 7
### Integrity check (checkval)
  We use CrcXmodem() to compute 16 bit (2 bytes) code to verify the integrity of the signal.  
  The input is the command messsage  
  example:
  from crccheck.crc import CrcXmodem  
  crc_checker = CrcXmodem()  
  crc_checker.calc(b'\x0c\x00\x07')  
  =1414
