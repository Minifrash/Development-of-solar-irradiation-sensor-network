import _thread
import time
from libraries.ram import *
from machine import UART, RTC
from struct import unpack
from libraries.ubx7 import *

class LocationSensor(object):

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
        self.conexion = 0
        self.sincro = False
        self.sampleThread = 0

    def confService(self, atributes):
        self.mode = atributes['mode']
        self.conexion = atributes['connectionService']
        self.frequency = atributes['frequency']
        self.uart = UART(1)
        self.ubx = ubx7(self.uart) # UBX7 device declaration
        self.cmd = ubx7msg() # commands to be sent to the ubx device
        self.res = ubx7msg() # responses to be received from the ubx device
        self.ack = ubx7msg() #   ack (or nak) to be received from the ubx device
	self.rtc = RTC()

    def start(self): # Tener un timeout o una manera de comprobar si hay un error y inizializar el rtc de otra forma y dar una posicion fija
        self.sampleThread = _thread.start_new_thread(self.sincroGPS, ())

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'mode':
            self.mode = newValue
        else:
            error = True # error de atributo incorrecto
        return error

    def sincroGPS(self):
        showMemoryRAM()
        if self.mode == 0:
            while(self.sincro == False and self.enabled == True):
                try:
                    self.res = self.ubx.sendrecv(NAV.PVT)
                    data = self.res.unpackpl('u4u2u1u1u1u1u1x1u4i4u1x1u1u1i4i4i4i4u4u4i4i4i4i4i4u4u4u2x2u4')
                    self.rtc.init((data[4],data[6],data[7],data[8]+1,data[9],data[10])) #year, month, day, hour+1(GMT+1), min, sec
                    self.longitude = data[24]
                    self.latitude = data[28]
                    self.height = data[32]
                    self.sincro = True
		    del data
                    data = dict() # Posiblemente añadir tambien la hora,min,sec en el diccionario
                    data.setdefault('hour', self.rtc.now()[3])
                    data.setdefault('minute', self.rtc.now()[4])
                    data.setdefault('seconds', self.rtc.now()[5])
                    data.setdefault('longitude', self.longitude)
                    data.setdefault('latitude', self.latitude)
                    data.setdefault('height', self.height)
                    self.conexion.sendPackage('sincroGPS', data)
                    collectRAM()
                    if self.sampleThread != 0:
                        print("MATO HILO")
                        _thread.exit()
                except:
                    if self.sincro == False: # por que salta una excepcion al matar el hilo
                        data = dict()
                        data.setdefault('hour', self.rtc.now()[3])
                        data.setdefault('minute', self.rtc.now()[4])
                        data.setdefault('seconds', self.rtc.now()[5])
                    	self.conexion.sendPackage('noSincroGPS', data)
                        print('Fallo GPS')
                    	time.sleep(self.frequency)
                collectRAM()

    def getData(self):
	return self.longitude, self.latitude, self.height

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False
