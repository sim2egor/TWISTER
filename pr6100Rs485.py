import minimalmodbus as MB

instrument1 = MB.Instrument('/dev/ttyUSB0', 1) #slave adress 1
#instrument2 = MB.Instrument('/dev/ttyUSB0', 2) #slave2 adress 2

# instrument1 = MB.Instrument('/dev/ttyAMA0', 1) #slave adress 1
# instrument2 = MB.Instrument('/dev/ttyAMA0', 2) #slave2 adress 2

instrument1.serial.baudrate = 9600
#instrument2.serial.baudrate = 9600

#registers
#0x2000 - register control
#0x2001 - register set frequency

#comands
#0x12 - FWDstart
#0x01 -  Stop
#0x22 - ReversStart

#ячейка 2000 - слово управления.
#бит 0 - стоп
#бит 1 - пуск
#бит 4 - прямо
#бит 5 - реверс

def Start_(Freq, slaveAdr, revers=0):
    #slaveAdr - 1 or 2
    #revers - 1 Active
    
    Freq = int(Freq*100)
    if (Freq >=0 and Freq <=40000):
        comand = 0x1E
        if (revers == 1) : comand = 0x2E
        
        if (slaveAdr == 1):
            instrument1.write_registers(0x2000, [comand,Freq])
            return 1
        else:
            if(slaveAdr == 2):
                instrument2.write_registers(0x2000, [comand,Freq])
                return 1
            
    else: return 0 #ERROR_Code Freq out the renge 0..400


def Stop_(slaveAdr):
    #slaveAdr - 1 or 2
    if (slaveAdr == 1):
        instrument1.write_registers(0x2000, [0x01,0x00])
        return 1
    else:
        if (slaveAdr == 2):
            instrument2.write_registers(0x2000, [0x01,0x00])
            return 1
        
def getFreq(slaveAdr):
    #There no fact ferq. There YSTANOVLENNAYA freq
    if (slaveAdr == 1):
        instrument1.read_register(0x0D09)/100
        return 1
    elif(slaveAdr == 2):
        instrument2.read_register(0x0D09)/100
        return 1
    
        
    
        
