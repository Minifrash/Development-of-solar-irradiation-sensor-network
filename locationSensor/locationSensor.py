import sys
import _thread
import time
import gc
import utime as time

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
        self.erCounter = 3
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

    def start(self): # Tener un timeout o una manera de comprobar si hay un error y inizializar el rtc de otra forma y dar una posicion fija
        #try:
            #self.sincroGPS()
	self.sampleThread = _thread.start_new_thread(self.sincroGPS, ())
	 #   gc.collect()
        #except:
	 #   gc.collect()
         #   print("Imposible conectar con GPS")# - Intento: " + str(counter))
            #mandar mensaje conxesion incorrecta
            #self.sampleThread = _thread.start_new_thread(self.sincroGPS, ())

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'mode':
            self.mode = newValue
        else:
            error = True # error de atributo incorrecto
        return error

    def sincroGPS(self):
        data = -1 # Posible error
        counter = 0
	print(_thread.stack_size(4096))
        #gc.collect()
        print('-----------------------------')
        print('GPS : Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
        print('-----------------------------')
        if self.mode == 0:
            while(self.sincro != True):
                try:
		    print("OK")
                    self.res = self.ubx.sendrecv(NAV.PVT)
                    data = self.res.unpackpl('u4u2u1u1u1u1u1x1u4i4u1x1u1u1i4i4i4i4u4u4i4i4i4i4i4u4u4u2x2u4')
                    self.rtc = RTC()
                    self.rtc.init((data[4],data[6],data[7],data[8],data[9],data[10])) #year, month, day, hour, min, sec
                    self.longitude = data[24]
                    self.latitude = data[28]
                    self.height = data[32]
                    self.sincro = True
		    gc.collect()
                    #mandar mensaje conxesion correcta
                    if self.sampleThread != 0:
			print("MATO HILO")
                        _thread.exit()
			print("NO MATO")
                except:
                    #mandar mensaje conxesion incorrecta
                 #   if counter < self.erCounter:
		#	gc.collect()
		#	print("Imposible conectar con GPS - Intento: " + str(counter))
		#	print('-----------------------------')
        	#	print('GPS : Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
        	#	print('-----------------------------')
                    #    counter += 1
                    #else:
		    print('-----------------------------')
		    print('GPS ANTES collect: Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
		    print('-----------------------------')
		    gc.collect()
		    print('-----------------------------')
		    print('GPS ANTES: Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
		    print('-----------------------------')
		    time.sleep(self.frequency)
		    gc.collect()
		    print('-----------------------------')
		    print('GPS DESPUES: Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
		    print('-----------------------------')

    def getData(self):
        #if self.sincro != True:
        #    try:
        #        self.sincroGPS()
        #        print("Conexion con GPS")
        #        print(self.rtc.now()) # Envio de mensaje de conexion con el gps y la hora actual del RTC despues de conexion al Servidor
        #    except:
        #        print("Imposible conectar con GPS") # Registro del fallo al modulo de gestion de errores
	return 0

    def getLocation(self):
    	#coordinates = dict()
    	#coordinates.setdefault('longitude', self.longitude)
    	#coordinates.setdefault('latitude', self.latitude)
    	#coordinates.setdefault('height', self.height)
        return self.longitude, self.latitude, self.height

    def printval(self, val, name, units='', scaling=1):
        print('{}: {} {}'.format(name, val*scaling, units))

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False


''' Papelera

    def demoGetData(self):
        data = -1 # Posible error
        if self.mode == 0:
            print("OK")
            self.res = self.ubx.sendrecv(NAV.PVT)
            print("OK2")
            data = self.res.unpackpl('u4u2u1u1u1u1u1x1u4i4u1x1u1u1i4i4i4i4u4u4i4i4i4i4i4u4u4u2x2u4')
            print("OK3")
            print(data[8])
            self.printval(data[0], 'iTOW', 'ms')
            self.printval(data[4], 'year')
            self.printval(data[6], 'month')
            self.printval(data[7], 'day')
            self.printval(data[8], 'hour')
            self.printval(data[9], 'min')
            self.printval(data[10], 'sec')
            self.printval(data[11], 'valid')
            self.printval(data[12], 'tAcc', 'ns')
            self.printval(data[16], 'nano', 'ns')
            self.printval(data[20], 'fixType')
            self.printval(data[21], 'flags')
            self.printval(data[22], 'reserved1')
            self.printval(data[23], 'numSV')
            self.printval(data[24], 'lon', 'deg', 1e-7)
            self.printval(data[28], 'lat', 'deg', 1e-7)
            self.printval(data[32], 'height', 'm', 1e-3)
            self.printval(data[36], 'hMSL', 'm', 1e-3)
            self.printval(data[40], 'hAcc', 'm', 1e-3)
            self.printval(data[44], 'vAcc', 'm', 1e-3)
            self.printval(data[48], 'velN', 'cm/s', 10)
            self.printval(data[52], 'velE', 'cm/s', 10)
            self.printval(data[56], 'velD', 'cm/s', 10)
            self.printval(data[60], 'gSpeed', 'cm/s', 10)
            self.printval(data[64], 'heading', 'deg', 1e-5)
            self.printval(data[68], 'sAcc', 'cm/s', 10)
            self.printval(data[72], 'headingAcc', 'deg', 1e-5)
            self.printval(data[76], 'pDOP', 'deg', 0.01)
            self.printval(data[78], 'reserved2')
            self.printval(data[80], 'reserved3')
            #data = #normal ¿Mandar array de lat-lon-alt?
        #elif self.mode == 1:
            #data = #rafaga ¿?
        else:
            data = -1
        return data
'''

