import serial # Import UART Module
import time
import ast


def crc16(data: str, poly: hex = 0xA001) -> str:
    '''
        CRC-16 MODBUS HASHING ALGORITHM
    '''
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc >> 1) ^ poly
                   if (crc & 0x0001)
                   else crc >> 1)

    hv = hex(crc).upper()[2:]
    blueprint = '0000'
    return (blueprint if len(hv) == 0 else blueprint[:-len(hv)] + hv)

def makeBytes(DID,FID,RIDH,RIDL,RVH,RVL):
    a = DID
    b = FID
    c = RIDH
    d = RIDL
    e = RVH
    f = RVL

    return bytes([a,b,c,d,e,f])

def CRC(DeviceID,FunctionID,RegIDH,RegIDL,RegValH,RegValL):
    CMDBytes = makeBytes(DeviceID,FunctionID,RegIDH,RegIDL,RegValH,RegValL)
    CRCResult = crc16(CMDBytes)

    print("CRC:",CRCResult)

    ts = int(CRCResult,16)
    L = ts & 0x00FF  # Low 8bit
    H = (ts & 0xFF00) >>8
    print (L)
    print (H)

    STR = bytearray(CMDBytes)

    STR.append(L)
    STR.append(H)

    return STR




def CSE_main(any):
    ser=serial.Serial('COM4', 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

    data = CRC(0x01, 0x04, 0x01, 0x00, 0x00, 0x08)
    print(data)

    result = ser.write(data)     #Write Data
    print("Total message: %d bytes" %(result))


    ser.close()     #Turn off UART







'''

def readSTA():  #read status
    a = 0x55      #Head Frame
    b = 0x55      #Head Frame
    c = 0x02      #
    d = 0x07      #

    print ("Stop action completed.")
    return bytes([a,b,c,d])

def Stop():
    a = 0x55      #Head Frame
    b = 0x55      #Head Frame
    c = 0x02      #
    d = 0x07      #

    print ("Stop action completed.")
    return bytes([a,b,c,d])


def main():
    ser=serial.Serial('COM3', 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

    motorID = 1

    data = makeSTR(motorID,0,1000)  #MotorID[1-3]; Position[0-65535]; Duration[0-65535]
    result = ser.write(data)     #Write Data
    print("Total message: %d bytes" %(result))
    time.sleep(1.5)
    data = makeSTR(motorID,1000,3000)         #MotorID[1-3]; Position[0-65535]; Duration[0-65535]
    result = ser.write(data)     #Write Data
    print("Total message: %d bytes" %(result))
    time.sleep(1.5)

    ser.close()     #Turn off UART

if __name__ == '__main__':
    main()
'''