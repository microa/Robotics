import serial # Import UART Module
import time

from Mid import GVar

class SDM():
    def __init__(self):
        pass


    def makeSTR(HandID,Position,Speed): #make strings. HandID[0,1,2]; Position[0~655535]; Speed[0-65535]--ms
        a = 0x55      #Head Frame
        b = 0x55      #Head Frame
        c = 0x08      #Data Lenth = How many Servo include * 3+5. This case = 1*3+5
        d = 0x03      #Servo move command[3:move;]
        e = 0x01      #How many Servo being control[1-3]

        f = Speed & 0x00FF                   #Low 8bit of time(Speed)
        g = Speed >> 8                       #High 8bit of time(Speed)
        print ("Real Moving Time: %d ms" %(Speed))

        h = HandID                               #MotorID

        i = Position & 0x00FF                #Low 8bit of target position
        j = Position >> 8                    #High 8bit of target position
        print ("Real Position is: %d 'd" %(Position))

        return bytes([a,b,c,d,e,f,g,h,i,j])

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

        a = GVar.GLB_CurrentPos[0] = RCV[6] + RCV[7] * 256
        b = GVar.GLB_CurrentPos[1] = RCV[9] + RCV[10] * 256
        if len(RCV) >= 13:
            c = GVar.GLB_CurrentPos[2] = RCV[12] + RCV[13] * 256
        else:
            c = GVar.GLB_CurrentPos[2] = RCV[12]
        return a,b,c

    def ctrlSpeed():  #control motion speed
        a = 0x55
        b = 0x55



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

    def MotorControl(MID,Pos,Speed):

        #Ser = Serial.Serial(GVar.SDF_Serial_Port, GVar.SDF_Serial_Baud, bytesize=Serial.EIGHTBITS, parity=Serial.PARITY_NONE,
        #                    stopbits=Serial.STOPBITS_ONE, timeout=1)

        motorID = MID


        '''
        if MID == 0: #bias 1:Standard 2:+50 3:+70
            Pos = Pos + GVar.GLB_ReferPos[0]
        if MID == 1: #bias 1:Standard 2:+50 3:+70
            Pos = Pos + GVar.GLB_ReferPos[1]
        if MID == 2:
            Pos = Pos + GVar.GLB_ReferPos[2]
        '''

        data = SDM.makeSTR(motorID, Pos, Speed)  # MotorID[1-3]; Position[0-65535]; Duration[0-65535]jiang
        result = Ser.write(data)  # Write Data
        print("Total message: %d bytes" % (result))



        #time.sleep((Time+500)/1000)

        #Ser.close()  # Turn off UART

    def SimuCtrl(Ser,motorID0,Pos0,motorID1,Pos1,motorID2,Pos2,Speed):

        #Ser = Serial.Serial(GVar.SDF_Serial_Port, GVar.SDF_Serial_Baud, bytesize=Serial.EIGHTBITS, parity=Serial.PARITY_NONE,
        #                    stopbits=Serial.STOPBITS_ONE, timeout=1)

        '''
        motorID0 = int(MID0[1]) + 1     #turning "M0" into 0, then plus 1
        motorID1 = int(MID1[1]) + 1
        motorID2 = int(MID2[1]) + 1
        '''

        '''
        #bias
        Pos0 = Pos0 + GVar.GLB_ReferPos[0]
        Pos1 = Pos1 + GVar.GLB_ReferPos[1]
        Pos2 = Pos2 + GVar.GLB_ReferPos[2]
        '''


        data = SDM.makeSTR(motorID0, Pos0, Speed)  # MotorID[1-3]; Position[0-65535]; Duration[0-65535]jiang
        result = Ser.write(data)  # Write Data
        print("Total message: %d bytes" % (result))

        data = SDM.makeSTR(motorID1, Pos1, Speed)  # MotorID[1-3]; Position[0-65535]; Duration[0-65535]jiang
        result = Ser.write(data)  # Write Data
        print("Total message: %d bytes" % (result))

        data = SDM.makeSTR(motorID2, Pos2, Speed)  # MotorID[1-3]; Position[0-65535]; Duration[0-65535]jiang
        result = Ser.write(data)  # Write Data
        print("Total message: %d bytes" % (result))



        #time.sleep((Time+500)/1000)

        #Ser.close()  # Turn off UART


    def Check_Overload(Ser):

        while 1:
            #t = time.time()
            a0,b0,c0 = SDM.readPOS(Ser)
            time.sleep(0.01)
            a1,b1,c1 = SDM.readPOS(Ser)
            am = a1 - a0
            bm = b1 - b0
            cm = c1 - c0
            print (am,bm,cm)
            if am<5 and bm<5 and cm<5:
                return 1
            else:
                return 0




    def SDF_main(q,x):

        Ser = serial.Serial("COM3", 9600, timeout=1)

        '''
        for i in range(len(GVar.Movement)):
            SDM.SimuCtrl(Ser,GVar.Movement[i][0], GVar.Movement[i][1], GVar.Movement[i][2], GVar.Movement[i][3],
                         GVar.Movement[i][4], GVar.Movement[i][5], GVar.Movement[i][6])   #1,2,3 means Motor ID
            time.sleep((GVar.Movement[i][7] + 300) / 1000)  #
        '''
        for i in range(30):

            SDM.SimuCtrl(Ser, GVar.Movement[0][0], GVar.Movement[0][1], GVar.Movement[0][2], GVar.Movement[0][3],
                         GVar.Movement[0][4], GVar.Movement[0][5], GVar.Movement[0][6])
            while 1:
                if GVar.Overload == 1:
                    #SDM.Stop(Ser)
                    #SDM.Stop(Ser)
                    SDM.SimuCtrl(Ser, GVar.Movement[1][0], GVar.Movement[1][1], GVar.Movement[1][2],
                                 GVar.Movement[1][3],
                                 GVar.Movement[1][4], GVar.Movement[1][5], GVar.Movement[1][6])
                    GVar.Overload = 0

                    break
            #time.sleep(GVar.holdingTime)
            time.sleep(0.1)
            SDM.SimuCtrl(Ser, GVar.Movement[1][0], GVar.Movement[1][1], GVar.Movement[1][2], GVar.Movement[1][3],
                         GVar.Movement[1][4], GVar.Movement[1][5], GVar.Movement[1][6])




            #SDM.Stop(Ser)
            #Stop(Ser)
            #SimuCtrl("M0", 150, "M1", 150, "M2", 150, 3000)
            #time.sleep(0.1)

            SDM.readPOS(Ser)
            time.sleep(0.1)

            SDM.SimuCtrl(Ser, GVar.Movement[1][0], GVar.Movement[1][1], GVar.Movement[1][2], GVar.Movement[1][3],
                         GVar.Movement[1][4], GVar.Movement[1][5], GVar.Movement[1][6])

            print(GVar.GLB_CurrentPos[0])
            print(GVar.GLB_CurrentPos[1])
            print(GVar.GLB_CurrentPos[2])

            time.sleep(0.1)

            SDM.SimuCtrl(Ser, GVar.Movement[1][0], GVar.Movement[1][1], GVar.Movement[1][2], GVar.Movement[1][3],
                         GVar.Movement[1][4], GVar.Movement[1][5], GVar.Movement[1][6])


            GVar.Nextround_Mark = 1
            time.sleep(3)


        Ser.close()  # Turn off UART





        #SimuCtrl("M0", 800, "M1", 800, "M2", 800, 3000)


