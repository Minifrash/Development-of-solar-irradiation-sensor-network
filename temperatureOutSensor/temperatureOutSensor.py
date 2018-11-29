import sys
import _thread
import time
import gc
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
        self.error = 0 #Codigo de error o cero si todo bien
        self.erCounter = 3 #Contador para reintentos tras error

    def confService(self, atributes):
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.powerPin(1)
        self.ow = OneWire(Pin('P4'))
        self.temp = DS18X20(self.ow) # DS18X20 must be powered on on instantiation (rom scan)
        self.powerPin(0)
        self.lock = atributes['lock']
        #print(self.lock)
        self.samplingFrequency = atributes['samplingFrequency']
        if not str(self.samplingFrequency).isdigit() or self.samplingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error
        self.mode = atributes['mode']
        if not str(self.mode).isdigit() or self.mode < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error

    def start(self):
        error = 0
        try:
            self.sampleThread = _thread.start_new_thread(self.sampling, ())
        except:
            error = -3 #CreateThread Error code
            #self.error = -3
        return error

    def sampling(self):
        while True:
            if self.enabled is True:
		time.sleep(self.samplingFrequency)
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
                if (self.lastTemperature < (-55.0) or self.lastTemperature > 125.0): #Si a la salida del bucle sigue siendo una mala muestra, se pasa a self.error
                    self.error = -11 #Incorrect Value Error code
                else:
                    self.sumTemperature += self.lastTemperature
                    self.sampleCounter += 1
		gc.collect()
                self.powerPin(0)
                self.lock.release()

            else:
                _thread.exit()

    def updateAtribute(self, atribute, newValue):
        error = 0
        if not str(newValue).isdigit() or newValue < 0: #¿Lo hace serviceManager?
            self.error = -9 #Incorrect AtributeValue Error
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            error = -8 # error de atributo incorrecto
            #self.error = -8 #Incorrect Atribute Error code
        return error

    def getData(self):
        data = 0 # Posible error
        self.lock.acquire()
        if self.mode == 0:
            try:
                data = self.sumTemperature/self.sampleCounter
            except ZeroDivisionError:
                error = -10
                #self.error = -10 #ZeroDivisionError code
        elif self.mode == 1:
            data = self.lastTemperature
        else:
            data = -9
            #self.error = -9 #Incorrect AtributeValue Error
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
