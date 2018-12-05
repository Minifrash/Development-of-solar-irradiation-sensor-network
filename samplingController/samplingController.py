import time
import gc
from machine import RTC
from machine import deepsleep
from batteryService.batteryService import BatteryService
from libraries.ram import *

class SamplingController(object):

    def __init__(self):
        self.serviceID = 1
        self.enabled = False
        self.sensorsList = dict()
        self.sendingFrequency = 0
        #self.sleepTime = ""
        #self.wakeTime = ""
        self.rtc = 0
        self.conexion = 0
        self.sleepTimeSeconds = 0
        self.wakeTimeSeconds = 0
        self.Battery = 0

    #Tratar posibles errores
    def confService(self, atributes):
        self.conexion = atributes['connectionService']
        self.sendingFrequency = atributes['sendingFrequency']
        self.sleepTimeSeconds = self.conversionTime(atributes['sleepTime'])
        self.wakeTimeSeconds = self.conversionTime(atributes['wakeTime'])
        self.sensorsList = atributes['sensorsList']
        #self.sleepTimeSeconds = self.conversionTime(self.sleepTime)
        #self.wakeTimeSeconds = self.conversionTime(self.wakeTime)
        self.rtc = RTC()
        self.Battery = BatteryService()
	self.Battery.connect()

    def start(self):
        self.sendData()

    def setServicesList(self, sensorsList):
        self.sensorsList = sensorsList

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'servicesList':
            self.servicesList = newValue
        elif atribute == 'sendingFrequency':
            self.sendingFrequency = newValue
        elif atribute == 'sleepTime':
            self.sleepTime = newValue
        elif atribute == 'wakeTime':
            self.wakeTime = newValue
        else:
            error = True # error de atributo incorrecto -8
        return error

    def sendData(self): # Modificar para enviar datos a mensajeriaSensor
	collectRAM()        
	showMemoryRAM()#self.ram()
     	i = 0
    	dataSend = 0# dict()
        while True:
            data = dict()
            time.sleep(self.sendingFrequency)
            print("-----------------------------------------------------------Iteracion numero = " + str(i) + "---------------------------------------------------------------")
            for sensor, valor in self.sensorsList.items():
            	muestra = valor.getData()
            	data.setdefault(sensor, muestra)
            	dataSend = str(sensor) + " : " + str(muestra)
                print(dataSend)
            	collectRAM()        
		showMemoryRAM()#self.ram()
		#self.ram()
            data.setdefault('Batt', self.Battery.getData())
            self.conexion.sendPackage('sample', data)
            del data
            collectRAM()        
	    showMemoryRAM()#self.ram()
            i += 1
	    print('SleepSeconds: ' + str(self.sleepTimeSeconds))
            if self.nowTimeInSeconds() >= self.sleepTimeSeconds:
                self.sleep()



    def connect(self, atributes):
        self.enabled = False
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False


    def sleep(self):
        timeToSleep = 0
        seconds = self.nowTimeInSeconds()
        if self.wakeTimeSeconds < self.sleepTimeSeconds:
            timeToSleep =  (86400 - seconds) + self.wakeTimeSeconds
        else:
            timeToSleep = self.wakeTimeSeconds - seconds #self.sleepTimeSeconds
	print('Duermo:' + str(timeToSleep))
	if timeToSleep >= 0:
            deepsleep(timeToSleep*1000)

    def conversionTime(self, timeData):
        auxTime = timeData.split(':')
        seconds = eval(auxTime[0]) * 3600
        seconds += eval(auxTime[1]) * 60
        seconds += eval(auxTime[2])
        return seconds

    def nowTimeInSeconds(self):
        seconds = self.rtc.now()[3] * 3600
        seconds += self.rtc.now()[4] * 60
        seconds += self.rtc.now()[5]
	print('NowSeconds: ' + str(seconds))
        return seconds

    ''' Funciones pendientes
    def wakeUp(self):
    '''

