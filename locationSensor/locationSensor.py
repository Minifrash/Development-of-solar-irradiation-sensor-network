import sys
import _thread
import time
from machine import UART
from struct import unpack
from locationSensor.ubx7 import *

class LocationSensor(object):

    def __init__(self):
        self.serviceID = 2
        self.mode = 0
        self.latitude = 0
        self.altitude = 0
        self.longitude = 0
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = 0 #_thread.start_new_thread(self.sampling, (self.samplingFrequency, 1))#0 # ¿Como inicializar?
        self.uart = 0
        self.ubx = 0
        self.cmd = 0
        self.res = 0
        self.ack = 0

    def confService(self, atributos):
        self.mode = 0#atributos['mode']
        self.uart = UART(1)
        self.ubx = ubx7(self.uart) # UBX7 device declaration
        self.cmd = ubx7msg() # commands to be sent to the ubx device
        self.res = ubx7msg() # responses to be received from the ubx device
        self.ack = ubx7msg() #   ack (or nak) to be received from the ubx device

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,2))

    '''def sincro(self):'''

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'mode':
            self.mode = newValue
        else:
            error = True # error de atributo incorrecto
        return error


    def getData(self):
        data = -1 # Posible error
        if self.mode == 0:
            print("OK")
            self.res = self.ubx.sendrecv(NAV.PVT)
            print("OK2")
            data = self.res.unpackpl('u4u2u1u1u1u1u1x1u4i4u1x1u1u1i4i4i4i4u4u4i4i4i4i4i4u4u4u2x2u4')
            print("OK3")
            printval(data[0], 'iTOW', 'ms')
            printval(data[4], 'year')
            printval(data[6], 'month')
            printval(data[7], 'day')
            printval(data[8], 'hour')
            printval(data[9], 'min')
            printval(data[10], 'sec')
            printval(data[11], 'valid')
            printval(data[12], 'tAcc', 'ns')
            printval(data[16], 'nano', 'ns')
            printval(data[20], 'fixType')
            printval(data[21], 'flags')
            printval(data[22], 'reserved1')
            printval(data[23], 'numSV')
            printval(data[24], 'lon', 'deg', 1e-7)
            printval(data[28], 'lat', 'deg', 1e-7)
            printval(data[32], 'height', 'm', 1e-3)
            printval(data[36], 'hMSL', 'm', 1e-3)
            printval(data[40], 'hAcc', 'm', 1e-3)
            printval(data[44], 'vAcc', 'm', 1e-3)
            printval(data[48], 'velN', 'cm/s', 10)
            printval(data[52], 'velE', 'cm/s', 10)
            printval(data[56], 'velD', 'cm/s', 10)
            printval(data[60], 'gSpeed', 'cm/s', 10)
            printval(data[64], 'heading', 'deg', 1e-5)
            printval(data[68], 'sAcc', 'cm/s', 10)
            printval(data[72], 'headingAcc', 'deg', 1e-5)
            printval(data[76], 'pDOP', 'deg', 0.01)
            printval(data[78], 'reserved2')
            printval(data[80], 'reserved3')
            #data = #normal ¿Mandar array de lat-lon-alt?
        #elif self.mode == 1:
            #data = #rafaga ¿?
        else:
            data = -1
        return data


    def disconnect(self):
        try:
            self.sampleThread = _thread.exit()
        except SystemExit:
            error = -1 #-1 es un ejemplo, dependerá de política de errores

    def info(self):
        print('Setting CFG.INF... ', end='')
        self.res = self.ubx.sendrecv(CFG.INF)
        data = self.res.unpackpl('u1u1u2x1')
        printval(data[0], 'protocolID')
        printval(data[1], 'reserved0')
        printval(data[2], 'reserved1')
        printval(data[4], 'infMsgMask')

        #self.cmd = ubx7msg.packpl(self.ubx, CFG.INF, {4: [36864, 'u4'], 8: [0, 'u4']}) ###!!! valor data[4]
        #self.ack = self.ubx.sendrecvcmd(self.cmd)
        #print('ACK: {} Valid: {}'.format(self.ack.CLASSID, self.ack.isvalid()))

    def setgnss():
        '''
        CFG-GNSS
        - Disable GLONASS blocks
        '''
        print('Setting CFG.GNSS... ', end='')
        res, ack = ubx.sendrecv(CFG.GNSS)
        nBlocks = (len(res.PAYLOAD) - 4)//8
        data = res.unpackpl('u1u1u1' + 'u1u1u1u1x4'*nBlocks)
        data2 = {}
        for N in range(nBlocks):
            if data[4 + 8*N] == 6:
                data2[8 + 8*N] = [0, 'x4']
                print('GLONASS block found!')
        cmd = ubx7msg.packpl(ubx, CFG.GNSS, data2)
        ack = ubx.sendrecvcmd(cmd)
        print('ACK: {} Valid: {}'.format(ack.CLASSID, ack.isvalid()))

    def setnav5(self):
        '''
        CFG-NAV5 Settings:
        - dynModel: Stationary
        - staticThresh: 10 cm/s
        '''
        print('Setting CFG.NAV5... ', end='')
        self.cmd = ubx7msg.packpl(self.ubx, CFG.NAV5, {2: [2, 'u1'], 22: [10, 'u1']})
        self.ack = self.ubx.sendrecvcmd(self.cmd)
        print('ACK: {} Valid: {}'.format(self.ack.CLASSID, self.ack.isvalid()))

    def setpm2(self):
        '''
        CFG-PM2 Settings:
        - updatePeriod: 0
        - On/Off operation
        '''
        print('Setting CFG.PM2... ', end='')
        self.cmd = ubx7msg.packpl(self.ubx, CFG.PM2, {4: [36864, 'u4'], 8: [0, 'u4']}) ###!!! valor data[4]
        self.ack = self.ubx.sendrecvcmd(self.cmd)
        print('ACK: {} Valid: {}'.format(self.ack.CLASSID, self.ack.isvalid()))

    def setrxm(self):
        '''
        CFG-RXM Settings:
        - lpMode: 1 (Power Save Mode)
        '''
        print('Setting CFG.RXM... ', end='')
        self.cmd = ubx7msg.packpl(self.ubx, CFG.RXM, {1: [1, 'u1']})
        print("Holi")
        self.ack = self.ubx.sendrecvcmd(self.cmd)
        print('ACK: {} Valid: {}'.format(self.ack.CLASSID, self.ack.isvalid()))

    def printval(val, name, units='', scaling=1):
        print('{}: {} {}'.format(name, val*scaling, units))

def main():
    location = LocationSensor()
    location.confService(0)
    location.getData()
    #location.setnav5()
    #location.setrxm()
    #location.info()

main()
