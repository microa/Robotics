import serial  # Import UART Module
import time
import pandas as pd
import string

from numpy import byte

from Mid import GVar




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


def makeBytes(DID, FID, RIDH, RIDL, RVH, RVL):
    a = DID
    b = FID
    c = RIDH
    d = RIDL
    e = RVH
    f = RVL

    return bytes([a, b, c, d, e, f])


def CRC(DeviceID, FunctionID, RegIDH, RegIDL, RegValH, RegValL):
    CMDBytes = makeBytes(DeviceID, FunctionID, RegIDH, RegIDL, RegValH, RegValL)
    CRCResult = crc16(CMDBytes)

    # print("CRC:", CRCResult)

    ts = int(CRCResult, 16)
    L = ts & 0x00FF  # Low 8bit
    H = (ts & 0xFF00) >> 8

    STR = bytearray(CMDBytes)

    STR.append(L)
    STR.append(H)

    return STR

'''
def hexstrConvert(hexstr0, hexstr1):
    hexstr0 = str(hexstr0)
    hexstr1 = str(hexstr1)
    # hexstr0 = hexstr0.replace("\\", "0")
    # hexstr1 = hexstr1.replace("\\", "0")
    transRCV_H = ''.join('%02x' % ord(c) for c in hexstr0)
    transRCV_L = ''.join('%02x' % ord(c) for c in hexstr1)
    transRCV_H = int(transRCV_H)
    transRCV_L = int(transRCV_L)
    transRCV = transRCV_H * 256 + transRCV_L
    return transRCV
'''
def hexstrConvert(hexstr0, hexstr1):
    transRCV_H = int(hexstr0)
    transRCV_L = int(hexstr1)

    transRCV = transRCV_H * 256 + transRCV_L
    return transRCV

def readModbus(ser, DeviceID, FunctionID, RegIDH, RegIDL, RegValH, RegValL):
    data = CRC(DeviceID, FunctionID, RegIDH, RegIDL, RegValH, RegValL)

    result = ser.write(data)  # Write Data
    print("Sent: %d bytes,detail: %s" % (result, data))

    # Receive message
    temp = bytes([])

    while True:
        if ser.in_waiting:
            RCV = ser.read(ser.in_waiting)
            #print (RCV)
            probe = crc16(bytes(RCV))
            if (probe == "0000"):  # Exit Marker
                print("Received:%d bytes: %s" % (len(RCV), RCV))
                break
            elif(temp != RCV):
                RCV = temp+ RCV
                temp = RCV
                print ("Reconstruction RCV Result: ", RCV)
                probe = crc16(bytes(RCV))
                if (probe == "0000"):  # Exit Marker
                    print("Received:%d bytes: %s" % (len(RCV), RCV))
                    break


    '''
    while True:
        recv = ser.readline()

        if recv == ''.encode():
            break;
        else:
            RCV = recv
            print("Received: %d bytes,detail: %s" % (len(recv), recv))
    '''
    return RCV


def readData():
    # build dataframe
    Dt = {'Timestamp': [],
          'ADW000_CH00': [],  # ART DAM-3128W 001, Channel00
          'ADW000_CH01': [],
          'ADW000_CH02': [],
          'ADW000_CH03': [],
          'ADW000_CH04': [],
          'ADW000_CH05': [],
          'ADW000_CH06': [],
          'ADW000_CH07': [],

          'ADW001_CH00': [],  # ART DAM-3128W 001, Channel00
          'ADW001_CH01': [],
          'ADW001_CH02': [],
          'ADW001_CH03': [],
          'ADW001_CH04': [],
          'ADW001_CH05': [],
          'ADW001_CH06': [],
          'ADW001_CH07': [],

          'ADW002_CH00': [],  # ART DAM-3128W 001, Channel00
          'ADW002_CH01': [],
          'ADW002_CH02': [],
          'ADW002_CH03': [],
          'ADW002_CH04': [],
          'ADW002_CH05': [],
          'ADW002_CH06': [],
          'ADW002_CH07': [],

          }

    df = pd.DataFrame(Dt)
    GVar.Gdf = df

    ser = serial.Serial(GVar.ADR_Serial_Port, GVar.ADR_Serial_Baud, timeout=1)

    # readModbus(ser, 0x03, 0x04, 0x01, 0x00, 0x00, 0x08)  #baud
    #01 10 00 84 00 02 04 00 01 00 07 EA 3E #Set Baudrate into GVar.ADR_Serial_Baud


    for i in range(GVar.ADC_Collect_Points):

        RCV000 = readModbus(ser, 0x01, 0x04, 0x01, 0x00, 0x00, 0x08)
        RCV001 = readModbus(ser, 0x02, 0x04, 0x01, 0x00, 0x00, 0x08)
        RCV002 = readModbus(ser, 0x03, 0x04, 0x01, 0x00, 0x00, 0x08)

        t = time.time()  ########################  TIME MARKER

        GVar.GM[0][0] = M0CH00 = hexstrConvert(RCV000[3], RCV000[4])
        GVar.GM[0][1] = M0CH01 = hexstrConvert(RCV000[5], RCV000[6])
        GVar.GM[0][2] = M0CH02 = hexstrConvert(RCV000[7], RCV000[8])
        GVar.GM[0][3] = M0CH03 = hexstrConvert(RCV000[9], RCV000[10])
        GVar.GM[0][4] = M0CH04 = hexstrConvert(RCV000[11], RCV000[12])
        GVar.GM[0][5] = M0CH05 = hexstrConvert(RCV000[13], RCV000[14])
        GVar.GM[0][6] = M0CH06 = hexstrConvert(RCV000[15], RCV000[16])
        GVar.GM[0][7] = M0CH07 = hexstrConvert(RCV000[17], RCV000[18])

        GVar.GM[1][0] = M1CH00 = hexstrConvert(RCV001[3], RCV001[4])
        GVar.GM[1][1] = M1CH01 = hexstrConvert(RCV001[5], RCV001[6])
        GVar.GM[1][2] = M1CH02 = hexstrConvert(RCV001[7], RCV001[8])
        GVar.GM[1][3] = M1CH03 = hexstrConvert(RCV001[9], RCV001[10])
        GVar.GM[1][4] = M1CH04 = hexstrConvert(RCV001[11], RCV001[12])
        GVar.GM[1][5] = M1CH05 = hexstrConvert(RCV001[13], RCV001[14])
        GVar.GM[1][6] = M1CH06 = hexstrConvert(RCV001[15], RCV001[16])
        GVar.GM[1][7] = M1CH07 = hexstrConvert(RCV001[17], RCV001[18])

        GVar.GM[2][0] = M2CH00 = hexstrConvert(RCV002[3], RCV002[4])
        GVar.GM[2][1] = M2CH01 = hexstrConvert(RCV002[5], RCV002[6])
        GVar.GM[2][2] = M2CH02 = hexstrConvert(RCV002[7], RCV002[8])
        GVar.GM[2][3] = M2CH03 = hexstrConvert(RCV002[9], RCV002[10])
        GVar.GM[2][4] = M2CH04 = hexstrConvert(RCV002[11], RCV002[12])
        GVar.GM[2][5] = M2CH05 = hexstrConvert(RCV002[13], RCV002[14])
        GVar.GM[2][6] = M2CH06 = hexstrConvert(RCV002[15], RCV002[16])
        GVar.GM[2][7] = M2CH07 = hexstrConvert(RCV002[17], RCV002[18])

        for x in range(3):
            for y in range(6):
                if GVar.GM[x][y+2] < GVar.overload_Limit_Var:
                    GVar.Overload = 1
                    print ("-----Warning!! Overload detected-----")

        df = df.append({'Timestamp': t,
                        'ADW000_CH00': M0CH00,
                        'ADW000_CH01': M0CH01,
                        'ADW000_CH02': M0CH02,
                        'ADW000_CH03': M0CH03,
                        'ADW000_CH04': M0CH04,
                        'ADW000_CH05': M0CH05,
                        'ADW000_CH06': M0CH06,
                        'ADW000_CH07': M0CH07,

                        'ADW001_CH00': M1CH00,
                        'ADW001_CH01': M1CH01,
                        'ADW001_CH02': M1CH02,
                        'ADW001_CH03': M1CH03,
                        'ADW001_CH04': M1CH04,
                        'ADW001_CH05': M1CH05,
                        'ADW001_CH06': M1CH06,
                        'ADW001_CH07': M1CH07,

                        'ADW002_CH00': M2CH00,
                        'ADW002_CH01': M2CH01,
                        'ADW002_CH02': M2CH02,
                        'ADW002_CH03': M2CH03,
                        'ADW002_CH04': M2CH04,
                        'ADW002_CH05': M2CH05,
                        'ADW002_CH06': M2CH06,
                        'ADW002_CH07': M2CH07,

                        }, ignore_index=True)

        #time.sleep(0.01)
        if GVar.Nextround_Mark ==1:
            GVar.Nextround_Mark =0
            df = df.append({'Timestamp': t,
                            'ADW000_CH00': 1111,
                            'ADW000_CH01': 1111,
                            'ADW000_CH02': 1111,
                            'ADW000_CH03': 1111,
                            'ADW000_CH04': 1111,
                            'ADW000_CH05': 1111,
                            'ADW000_CH06': 1111,
                            'ADW000_CH07': 1111,

                            'ADW001_CH00': 1111,
                            'ADW001_CH01': 1111,
                            'ADW001_CH02': 1111,
                            'ADW001_CH03': 1111,
                            'ADW001_CH04': 1111,
                            'ADW001_CH05': 1111,
                            'ADW001_CH06': 1111,
                            'ADW001_CH07': 1111,

                            'ADW002_CH00': 1111,
                            'ADW002_CH01': 1111,
                            'ADW002_CH02': 1111,
                            'ADW002_CH03': 1111,
                            'ADW002_CH04': 1111,
                            'ADW002_CH05': 1111,
                            'ADW002_CH06': 1111,
                            'ADW002_CH07': 1111,

                            }, ignore_index=True)




    ser.close()  # Turn off UART

    df.to_csv(r'ISRL_3F_Data.csv', index=False, header=True)

    print("file exported.")


def ADR_main(q,x):
    readData()
    #print (any)




'''
    ser=serial.Serial('COM8', 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

    data = CRC(0x01, 0x04, 0x01, 0x00, 0x00, 0x08)
    print(data)

    result = ser.write(data)     #Write Data
    print("Total message: %d bytes" %(result))

    ser.close()     #Turn off UART
    '''

'''
import serial # Import UART Module
import math
import sys
import threading
import pandas as pd
import re
import csv
import time
import datetime
import matplotlib.pyplot as plt

global Red,Green,Blue

def Convert(Original):

    matchR = re.search("R:", Original)
    matchG = re.search("G:", Original)
    matchB = re.search("B:", Original)


    if matchR and matchG and matchB:
        posR = matchR.span()
        posG = matchG.span()
        posB = matchB.span()

        #print(posR,posG,posB)

        Red = Original[posR[1]:posG[1] - 2]
        Green = Original[posG[1]:posB[1] - 2]
        Blue = Original[posB[1]:posB[1] + 3]
    else:
        Red,Green,Blue = None,None,None

    return Red,Green,Blue


def UART_Output():
    ser = serial.Serial('COM3', 9600, timeout=1)


    result = ser.write('AT\r\n'.encode("UTF8"))  # Write Data
    print("Total message: %d bytes" % (result))

    # Receive message
    while True:
        recv = ser.readline().decode()
        print(recv)
        if str(recv) == 'OK\r\n':
            break

    Dt = {'Timestamp': [],
          'R': [],
          'G': [],
          'B': []
          }
    df = pd.DataFrame(Dt)

    rx = []
    ry = []
    gx = []
    gy = []
    bx = []
    by = []
    plt.ion()

    for i in range(400):
        result = ser.write('AT+COLOR\r\n'.encode("UTF8"))  # Write Data
        print("Total message: %d bytes" % (result))

        # Receive message
        while True:
            recv = ser.readline().decode()
            print (recv)
            if str(recv) != 'OK\r\n':
                Red,Green,Blue = Convert(recv)
            if str(recv) == 'OK\r\n':
                break

        Red = int(Red)
        Green = int(Green)
        Blue = int(Blue)

        t = time.time()    ########################  TIME MARKER

        df = df.append({'Timestamp': t,
                        'R': Red,
                        'G': Green,
                        'B': Blue
                        }, ignore_index=True)

        rx.append(t)
        ry.append(Red)
        gx.append(t)
        gy.append(Green)
        bx.append(t)
        by.append(Blue)
        plt.clf()
        plt.plot(rx, ry, color = 'red')
        plt.plot(gx, gy, color = 'green')
        plt.plot(bx, by, color = 'blue')
        plt.pause(0.2)
        #plt.ion()
        #line = plt.plot(x,y)
    #df.plot('Timestamp')
    #plt.show()
    df.to_csv(r'ColorSensor.csv', index=False, header=True)



    ser.close()  # Turn off UART



def main():
    UART_Output()
    #UART_Read()
if __name__ == '__main__':
    main()

'''
