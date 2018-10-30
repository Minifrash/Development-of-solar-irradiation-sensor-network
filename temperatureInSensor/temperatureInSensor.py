import sys
import _thread
import time
from libraries.dht import DHT

class TemperatureInSensor(object):

    def __init__(self):
        self.serviceID = 4
        self.samplingFrequency = 0
        self.mode = 0
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.enabled = False
        self.sampleThread = 0
        self.temp = 0#DHT('P3',1)
        self.dht = 0
        self.lock = 0
        self.error = 0

    def confService(self, atributes):
        self.temp = DHT('P3',1)
        self.lock = lock
        self.dht = dht
        self.samplingFrequency = atributes['samplingFrecuency']
        if not self.samplingFrequency.isdigit() or self.samplingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error
        self.mode = atributes['mode']
        if not self.mode.isdigit() or self.mode < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error

    def start(self):
        self.dht.connect(self.serviceID, self.samplingFrequency, self.lock)

    def updateAtribute(self, atribute, newValue):
        error = 0
        if not newValue.isdigit() or newValue < 0: #¿Lo hace serviceManager?
            self.error = -9 #Incorrect AtributeValue Error
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            error = -8 # error de atributo incorrecto
        return error

    def getData(self):
        data = self.dht.getTemperature(self.mode)
        return data

    def disconnect(self):
        self.enabled = False
        self.dht.disconnect(self.serviceID)

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes, dht, lock)
        self.start()

    def serviceEnabled(self):
        return self.enabled
