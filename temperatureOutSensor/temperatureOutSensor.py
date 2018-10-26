import sys
import _thread
import time
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
        self.powerPin = 0 #Pin('P8', mode=Pin.OUT)
        self.ow = 0 #OneWire(Pin('P4'))
        self.temp = 0 #DS18X20(self.ow) # DS18X20 must be powered on on instantiation (rom scan)
        self.error = 0
        self.erCounter = 3

    def confService(self, atributes):
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.powerPin(1)
        self.ow = OneWire(Pin('P4'))
        self.temp = DS18X20(self.ow) # DS18X20 must be powered on on instantiation (rom scan)
        self.powerPin(0)
        self.samplingFrequency = atributes['samplingFrecuency']
        #Comprobar si es un numero (isdigit) y si es negativo
        self.mode = atributes['mode']
        #Comprobar si es un numero (isdigit) y si es negativo

    def start(self):
        # Crear el thread para la funcion sendData()
        try:
            self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,6))
        except:
            self.error = -3 #CreateThread Error code

    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                self.powerPin(1)
                self.temp.start_convertion()
                time.sleep(delay)
                self.lastTemperature = self.temp.read_temp_async()
                #Bucle de lecturas si se cumple el siguiente if
                count = 0
                while((self.lastTemperature < (-55.0) or self.lastTemperature > 125.0) and count < self.erCounter):
                    self.lastTemperature = self.temp.read_temp_async()
                    count += 1
                if (self.lastTemperature < (-55.0) or self.lastTemperature > 125.0): #Si a la salida del bucle sigue siendo una mala muestra, se pasa a self.error
                    self.error = -11 #Incorrect Value Error code
                else:
                    self.sumTemperature += self.lastTemperature
                    self.sampleCounter += 1
                self.powerPin(0)
            else:
                try:
                    _thread.exit()
                except SystemExit:
                    self.error = -4 #SystemExit code

    def updateAtribute(self, atribute, newValue):
        error = 0
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            error = -8 # error de atributo incorrecto
            self.error = -8 #Incorrect Atribute Error code
        return error #devolver self.error?

    def getData(self):
        data = -1 # Posible error
        if self.mode == 0:
            try:
                data = self.sumTemperature/self.sampleCounter
            except ZeroDivisionError:
                self.error = -10 #ZeroDivisionError code
        elif self.mode == 1:
            data = self.lastTemperature
        else:
            data = -1
        self.sumTemperature = 0
        self.sampleCounter = 0
        return data

    def disconnect(self):
        self.enabled = False

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def serviceEnabled(self):
        return self.enabled
