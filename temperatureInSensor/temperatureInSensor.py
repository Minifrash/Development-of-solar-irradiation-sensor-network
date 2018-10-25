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

    def confService(self, atributes):
        #self.temp = DHT('P3',1)
        self.samplingFrequency = atributes['samplingFrecuency']
        self.mode = atributes['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        #self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,4))
        self.dh.start()

    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                time.sleep(delay)
                result = self.temp.read()
                self.lastTemperature = result.temperature/1.0
                self.sumTemperature += self.lastTemperature
                self.sampleCounter += 1
            else:
                _thread.exit()

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
        #data = -1 # Posible error
        #if self.mode == 0:
        #    data = self.sumTemperature/self.sampleCounter
        #elif self.mode == 1:
        #    data = self.lastTemperature
        #else:
        #    data = -1
        #self.sumTemperature = 0
        #self.sampleCounter = 0
        data = self.dh.getTemperature(self.mode)
        return data

    def disconnect(self):
        self.enabled = False
        self.dh.disconnect()

    def connect(self, atributes, dh):
        self.dh = dh
        self.enabled = True
        dh.connect()
        self.confService(atributes)
        self.start()

    def serviceEnabled(self):
        return self.enabled
