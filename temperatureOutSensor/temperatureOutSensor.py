import _thread
import time
from libraries.memoryManager import *
from machine import Pin
from libraries.onewire import DS18X20
from libraries.onewire import OneWire

class TemperatureOutSensor(object):

    def __init__(self):
        self.serviceID = 6
        self.samplingFrequency = 0
        self.mode = 0
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.enabled = False
        self.sampleThread = 0
        self.powerPin = 0
        self.ow = 0
        self.temp = 0
        self.lock = 0
        self.erCounter = 3
        self.errorLogService = 0

    def confService(self, atributes):
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.powerPin(1)
        self.ow = OneWire(Pin('P4'))
        self.temp = DS18X20(self.ow) # DS18X20 must be powered on on instantiation (rom scan)
        self.powerPin(0)
        self.lock = atributes['lock']
        self.samplingFrequency = atributes['samplingFrequency']
        self.errorLogService = atributes['errorLogService']
        self.mode = atributes['mode']
        if not str(self.samplingFrequency).isdigit() or self.samplingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        if not str(self.mode).isdigit() or self.mode < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error

    def start(self):
        try:
            self.sampleThread = _thread.start_new_thread(self.sampling, ())
        except:
            self.errorLogService.regError(self.serviceID, -3) #CreateThread Error code

    def sampling(self):
        while True:
            if self.enabled is True:
                time.sleep(self.samplingFrequency-0.751)#time.sleep(self.samplingFrequency)
                self.lock.acquire()
                self.powerPin(1)
                time.sleep(0.001)
                self.temp.start_convertion()
                time.sleep(0.75)
                self.lastTemperature = self.temp.read_temp_async()
                count = 0
                #Valores para sensor DS18X20
                while((self.lastTemperature < (-55.0) or self.lastTemperature > 125.0) and count < self.erCounter):
                    self.lastTemperature = self.temp.read_temp_async()
                    count += 1
                if (self.lastTemperature < (-55.0) or self.lastTemperature > 125.0): #Si a la salida del bucle sigue siendo una mala muestra, se pasa error
                    self.errorLogService.regError(self.serviceID, -11) #Incorrect Value Error code
                else:
                    self.sumTemperature += self.lastTemperature
                    self.sampleCounter += 1
                collectMemory()
                self.powerPin(0)
                self.lock.release()
            else:
                _thread.exit()

    def updateAtribute(self, atribute, newValue):
        if not str(newValue).isdigit() or newValue < 0:
            self.errorLogService.regError(self.serviceID, -9 ) #Incorrect AtributeValue Error
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            self.errorLogService.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def getData(self):
        data = 0 # En caso de error retorna 0
        self.lock.acquire()
        if self.mode == 0:
            try:
                data = self.sumTemperature/self.sampleCounter
            except ZeroDivisionError:
                self.errorLogService.regError(self.serviceID, -10) #ZeroDivisionError code
        elif self.mode == 1:
            data = self.lastTemperature
        else:
            self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.lock.release()
        return data

    def disconnect(self):
        self.enabled = False

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def serviceEnabled(self):
        return self.enabled
