import sys
import _thread
import time
from machine import Pin
from temperatureOutSensor.onewire import DS18X20
from temperatureOutSensor.onewire import OneWire

class TemperatureOutSensor(object):

    def __init__(self):
        self.serviceID = 6
        self.samplingFrequency = 0
        self.mode = 0
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = 0 #_thread.start_new_thread(self.sampling, (self.samplingFrequency, 1))#0 # ¿Como inicializar?
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.powerPin(1)
        self.ow = OneWire(Pin('P4'))
        self.temp = DS18X20(self.ow) # DS18X20 must be powered on on instantiation (rom scan)
        self.powerPin(0)


    def confService(self, atributos):
        self.samplingFrequency = atributos['samplingFrecuency']
        self.mode = atributos['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,6))

    def sampling(self, delay, id):
        while True:
            self.powerPin(1)
            #time.sleep(delay)
            self.temp.start_convertion()
            time.sleep(delay)
            self.lastTemperature = self.temp.read_temp_async()
            self.sumTemperature += self.lastTemperature
            self.sampleCounter += 1
            self.powerPin(0)

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            error = True # error de atributo incorrecto
        return error


    def getData(self):
        data = -1 # Posible error
        if self.mode == 0:
            data = self.sumTemperature/self.sampleCounter
        elif self.mode == 1:
            data = self.lastTemperature
        else:
            data = -1
        self.sumTemperature = 0
        self.sampleCounter = 0
        return data

    def disconnect(self):
        self.sampleThread.exit()

    ''' Funciones Pendientes

    def connect(self):

    def serviceEnabled(self):
        return enabled
    '''
