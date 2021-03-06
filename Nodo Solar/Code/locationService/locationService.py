import _thread
import time
from libraries.memoryManager import *
from machine import UART, RTC
from struct import unpack
from libraries.ubx7 import *

class LocationService(object):

    def __init__(self):
        self.serviceID = 2
        self.enabled = False
        self.mode = 0
        self.latitude = 0
        self.height = 0
        self.longitude = 0
        self.frequency = 0
        self.uart = 0
        self.ubx = 0
        self.cmd = 0
        self.res = 0
        self.ack = 0
        self.rtc = 0
        self.connectionService = 0
        self.sincro = False
        self.sampleThread = 0
        self.errorLogService = 0

    def confService(self, atributes):
        self.connectionService = atributes['connectionService']
        self.errorLogService = atributes['errorLogService']
        self.uart = UART(1)
        self.ubx = ubx7(self.uart) # UBX7 device declaration
        self.cmd = ubx7msg() # commands to be sent to the ubx device
        self.res = ubx7msg() # responses to be received from the ubx device
        self.ack = ubx7msg() #   ack (or nak) to be received from the ubx device
        self.rtc = RTC()
        if ('mode' in atributes) and ('frequency' in atributes):
            if not str(atributes['frequency']).isdigit() or atributes['frequency'] < 0: #Comprobar si es un numero (isdigit) y si es negativo
                self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
            else:
                self.frequency = atributes['frequency']
            if not str(atributes['mode']).isdigit() or atributes['mode'] < 0: #Comprobar si es un numero (isdigit) y si es negativo
                self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
            else:
                self.mode = atributes['mode']
        else:
            self.errorLogService.regError(self.serviceID, -2) #ConfFile Error

    def start(self):
        self.sampleThread = _thread.start_new_thread(self.sincroGPS, ())

    def updateAtribute(self, atribute, newValue):
        if atribute == 'mode':
            self.mode = newValue
        elif atribute == 'frequency':
            self.frequency = newValue
        else:
            self.errorLogService.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def sincroGPS(self):
        if self.mode == 0:
            while(self.sincro == False and self.enabled == True):
                try:
                    self.res = self.ubx.sendrecv(NAV.PVT)
                    data = self.res.unpackpl('u4u2u1u1u1u1u1x1u4i4u1x1u1u1i4i4i4i4u4u4i4i4i4i4i4u4u4u2x2u4')
                    self.rtc.init((data[4],data[6],data[7],data[8]+1,data[9],data[10])) #year, month, day, hour, min, sec
                    self.longitude = data[24]
                    self.latitude = data[28]
                    self.height = data[32]
                    self.sincro = True
                    del data
                    data = dict()
                    data.setdefault('hour', self.rtc.now()[3])
                    data.setdefault('minute', self.rtc.now()[4])
                    data.setdefault('seconds', self.rtc.now()[5])
                    self.connectionService.sendPackage('time', data)
                    data.setdefault('longitude', self.longitude)
                    data.setdefault('latitude', self.latitude)
                    data.setdefault('height', self.height)
                    self.connectionService.sendPackage('location', data)
                    collectMemory()
                    if self.sampleThread != 0:
                        _thread.exit()
                except:
                    if self.sincro == False:
                        self.errorLogService.regError(self.serviceID, -12) #Location Error
                    	time.sleep(self.frequency)
                collectMemory()

    def getData(self):
        return self.longitude, self.latitude, self.height

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False

    def serviceEnabled(self):
        return self.enabled
