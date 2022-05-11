import serial # Import UART Module
import time
from Mid import GVar

class STG():
    def __init__(self):
        pass

    def makeSTR_readPOS():  #read status
        a = 0x55      #Head Frame
        b = 0x55      #Head Frame
        c = 0x06      #control 3 motors then:3 + 3(static) = 6
        d = 0x15      #control ID(protocal by Hiwonder)
        e = 0x03      #3 motors
        f = 0x01      #Motor ID
        g = 0x02      #Motor ID
        h = 0x03      #Motor ID

        print ("Position read command completed.")
        return bytes([a,b,c,d,e,f,g,h])

    def readPOS(Ser):

        #Ser = Serial.Serial(GVar.SDF_Serial_Port, GVar.SDF_Serial_Baud, bytesize=Serial.EIGHTBITS, parity=Serial.PARITY_NONE,
        #                    stopbits=Serial.STOPBITS_ONE, timeout=1)

        data = SDM.makeSTR_readPOS()
        result = Ser.write(data)  # Write Data
        # print("Sent: %d bytes,detail: %s" % (result, data))

        RCV = 0
        while True:
            if Ser.in_waiting:
                RCT = Ser.read(Ser.in_waiting)
                if RCV == 0:
                    RCV = RCT
                else:
                    RCV = RCV + RCT
                # print (RCV)
                if len(RCV) > 13:
                    break

        GVar.GLB_CurrentPos[0] = RCV[6] + RCV[7] * 256
        GVar.GLB_CurrentPos[1] = RCV[9] + RCV[10] * 256
        if len(RCV) >= 13:
            GVar.GLB_CurrentPos[2] = RCV[12] + RCV[13] * 256
        else:
            GVar.GLB_CurrentPos[2] = RCV[12]



    def Stop(Ser):
        '''
        a = 0x55      #Head Frame
        b = 0x55      #Head Frame
        c = 0x02      #
        d = 0x07      #
        '''

        SDM.readPOS(Ser)


        SDM.SimuCtrl(Ser,1, GVar.GLB_CurrentPos[0], 2, GVar.GLB_CurrentPos[1], 3, GVar.GLB_CurrentPos[2], 200)

        #print("Stop action command sent: %d bytes" % (result))


    def STG_main(q,x):


        pass


