import time
from machine import RTC, deepsleep, Timer
from batteryService.batteryService import BatteryService
from libraries.ram import *

class SamplingController(object):

    def __init__(self):
        self.serviceID = 1
        self.enabled = False
        self.sensorsList = dict()
        self.sendingFrequency = 0
        self.rtc = 0
        self.conexion = 0
        self.sleepTimeSeconds = 0
        self.wakeTimeSeconds = 0
        self.Battery = 0
        self.alarm = 0
        self.errorLog = 0

    #Tratar posibles errores
    def confService(self, atributes):
        self.conexion = atributes['connectionService']
        self.sendingFrequency = atributes['sendingFrequency']
        if not str(self.sendingFrequency).isdigit() or self.sendingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        if self.checkValidTime(atributes['sleepTime']) == True:
            self.sleepTimeSeconds = self.conversionTime(atributes['sleepTime'])
        else:
            self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        if self.checkValidTime(atributes['sleepTime']) == True:
            self.wakeTimeSeconds = self.conversionTime(atributes['wakeTime'])
        else:
            self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        self.sensorsList = atributes['sensorsList']
        self.rtc = RTC()
        self.Battery = BatteryService()
        self.Battery.connect()
        self.errorLog = atributes['errorLog']

    def start(self):
        self.sendData()

    def setSensorsList(self, sensorsList):
        self.sensorsList = sensorsList

    def updateAtribute(self, atribute, newValue):
        if atribute == 'servicesList':
            self.servicesList = newValue
        elif atribute == 'sendingFrequency':
            if not str(newValue).isdigit() or newValue < 0:
            	self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
            	self.sendingFrequency = newValue
        elif atribute == 'sleepTime':
            if self.checkValidTime(newValue) == True:
                self.sleepTimeSeconds = self.conversionTime(newValue)
            else:
                self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        elif atribute == 'wakeTime':
            if self.checkValidTime(newValue) == True:
                self.wakeTimeSeconds = self.conversionTime(newValue)
            else:
                self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        else:
            self.errorLog.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def sendData(self):
        collectRAM()
        #showMemoryRAM()
     	i = 0
        #chrono = Timer.Chrono()
        timeChrono = 0
        while i<10:#self.enabled == True:
            dataSend = dict()
            if (self.sendingFrequency - timeChrono) > 0:
            	time.sleep(self.sendingFrequency-timeChrono)
            #chrono.start()
            dataSend.setdefault('hour', self.rtc.now()[3])
            dataSend.setdefault('minute', self.rtc.now()[4])
            dataSend.setdefault('seconds', self.rtc.now()[5])
            #print("Hora -> " + str(dataSend['hour']))
            #print("Minutos -> " + str(dataSend['minute']))
            #print("Segundos -> " + str(dataSend['seconds']))
            #print("-----------------------------------------------------------Iteracion numero = " + str(i) + "---------------------------------------------------------------")
            for sensor, valor in self.sensorsList.items():
            	sample = valor.getData()
            	dataSend.setdefault(sensor, sample)
            	#print(str(sensor) + " : " + str(sample))
            collectRAM()
            #showMemoryRAM()
            dataSend.setdefault('Batt', self.Battery.getData())
            #chrono.stop()
            #timeChrono = chrono.read()
            #chrono.reset()
            self.conexion.sendPackage('sample', dataSend)
            #self.conexion.disconnect()
            #print(total)#print('Crono: ' + str(total))
            del dataSend
            collectRAM()
            #showMemoryRAM()
            i += 1
            self.sleepPrueba()#self.sleep()

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False

    def sleepPrueba(self): # REPASAR
        timeToSleep = 0
        seconds = self.nowTimeInSeconds()
        if (seconds < self.wakeTimeSeconds and seconds >= self.sleepTimeSeconds) or (seconds < self.wakeTimeSeconds and seconds >= self.sleepTimeSeconds) :
            timeToSleep = self.wakeTimeSeconds - seconds
            print('Duermo:' + str(timeToSleep))
            if timeToSleep >= 0:
                deepsleep(timeToSleep*1000)
        if seconds > self.wakeTimeSeconds and seconds >= self.sleepTimeSeconds:
			timeToSleep =  (86400 - seconds) + self.wakeTimeSeconds
			print('Duermo:' + str(timeToSleep))
            if timeToSleep >= 0:
                deepsleep(timeToSleep*1000)

    def sleep(self): # REPASAR
        timeToSleep = 0
        seconds = self.nowTimeInSeconds()
        if seconds < self.wakeTimeSeconds and seconds >= self.sleepTimeSeconds:
            timeToSleep = self.wakeTimeSeconds - seconds
            print('Duermo:' + str(timeToSleep))
            if timeToSleep >= 0:
                deepsleep(timeToSleep*1000)
        if seconds > self.wakeTimeSeconds and seconds >= self.sleepTimeSeconds:
            if self.wakeTimeSeconds < self.sleepTimeSeconds:
                timeToSleep =  (86400 - seconds) + self.wakeTimeSeconds
            else:
                timeToSleep = self.wakeTimeSeconds - seconds
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
        return seconds

    def checkValidTime(self, timeData):
        validTime = True
        auxTime = timeData.split(':')
        if (eval(auxTime[0]) < 00) or (eval(auxTime[0]) > 24):
            validTime = False
        if (eval(auxTime[1]) < 00) or (eval(auxTime[1]) > 60):
            validTime = False
        if (eval(auxTime[2]) < 00) or (eval(auxTime[2]) > 60):
            validTime = False
        return validTime
