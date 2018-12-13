import _thread
import time
from machine import Pin
from libraries.dht import DHT
from libraries.ram import *

class DHT22(object):

    def __init__(self):
        self.enabledHumidity = False
        self.lastHumidity = 0
        self.sumHumidity = 0
        self.sampleCounterHumidity = 0
        self.enabledTemperature = False
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounterTemperature = 0
        self.samplingFrequency = 1
        self.sampleThread = 0
        self.powerPin = 0
        self.dht = 0
        self.lock = 0
        self.enabled = False
        self.errorLog = 0
        self.erCounter = 3

    def conf(self, atributes):
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.samplingFrequency = atributes['samplingFrequency']
        self.dht = DHT('P3',1)
	self.errorLog = atributes['errorLog']

    def start(self):
        if self.sampleThread == 0:
            try:
                self.sampleThread = _thread.start_new_thread(self.sampling, ())
            except:
                self.errorLog.regError(self.serviceID, -3) #CreateThread Error code

    def sampling(self):
        while True:
            if self.enabled == True:
                time.sleep(self.samplingFrequency-0.8) #time.sleep(self.samplingFrequency)
                self.lock.acquire()
                self.powerPin(1)
                time.sleep(0.8)
                result = self.dht.read()
                if self.enabledHumidity is True:
                    count = 0
                    while((result.humidity < 0.0 or result.humidity > 100.0) and count < self.erCounter):
                        time.sleep(0.375)
                        result = self.dht.read()
                        count += 1
                    if (result.humidity < 0.0 or result.humidity > 100.0): #Si a la salida del bucle sigue siendo una mala muestra, se pasa a self.errorLog
                        self.errorLog.regError(self.serviceID, -11)#Incorrect Value Error code
                    self.lastHumidity = result.humidity
                    self.sumHumidity += self.lastHumidity
                    self.sampleCounterHumidity += 1
                if self.enabledTemperature is True:
                    count = 0
                    while((result.temperature < (-40.0) or result.temperature > 125.0) and count < self.erCounter):
                        time.sleep(0.375)
                        result = self.dht.read()
                        count += 1
                    if (result.temperature < (-40.0) or result.temperature > 125.0): #Si a la salida del bucle sigue siendo una mala muestra, se pasa a self.errorLog
                        self.errorLog.regError(self.serviceID, -11)#Incorrect Value Error code
                    self.lastTemperature = result.temperature
                    self.sumTemperature += self.lastTemperature
                    self.sampleCounterTemperature += 1
                collectRAM()
                self.powerPin(0)
                self.lock.release()
            else:
                _thread.exit()


    def getHumidity(self, mode):
        data = 0 # En caso de error retorna 0 
        self.lock.acquire()
        if self.enabledHumidity is True:
            if mode == 0:
                try:
                    data = self.sumHumidity/self.sampleCounterHumidity
                except ZeroDivisionError:
                    self.errorLog.regError(self.serviceID, -10) #ZeroDivisionError code
            elif mode == 1:
                data = self.lastHumidity
            else:
                self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
            self.sumHumidity = 0
            self.sampleCounterHumidity = 0
        self.lock.release()
        return data

    def getTemperature(self, mode):
        data = 0 # En caso de error retorna 0 
        self.lock.acquire()
        if self.enabledTemperature is True:
            if mode == 0:
                try:
                    data = self.sumTemperature/self.sampleCounterTemperature
                except ZeroDivisionError:
                    self.errorLog.regError(self.serviceID, -10) #ZeroDivisionError code
            elif mode == 1:
                data = self.lastTemperature
            else:
                self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
            self.sumTemperature = 0
            self.sampleCounterTemperature = 0
        self.lock.release()
        return data

    def connect(self, atributes):
        if atributes['serviceID'] == 4 and self.enabledTemperature is False:
            self.enabledTemperature = True
        if atributes['serviceID'] == 5 and self.enabledHumidity is False:
            self.enabledHumidity = True
        if self.enabled is False:
            self.enabled = True
            self.lock = atributes['lock']
            self.conf(atributes)
            self.start()

    def disconnect(self, serviceID):
        if serviceID == 4 and self.enabledTemperature == True:
            self.enabledTemperature = False
        elif serviceID == 5 and self.enabledHumidity == True:
            self.enabledHumidity = False
        else:
            self.errorLog.regError(self.serviceID, -7) #Fallo en el serviceID o ya esta desconectado #Non-Active Service Error

        if self.enabledTemperature == False and self.enabledHumidity == False:
            self.sampleThread = 0
            self.enabled = False
