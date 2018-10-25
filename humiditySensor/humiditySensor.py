import sys
import _thread
import time
import gc
from libraries.dht import DHT

class HumiditySensor(object):

    def __init__(self):
        self.serviceID = 5
        self.samplingFrequency = 0
        self.mode = 0
        self.lastHumidity = 0
        self.sumHumidity = 0
        self.sampleCounter = 0
        self.enabled = False
        self.sampleThread = 0
        self.humidity = 0#DHT('P3',1)

    def confService(self, atributes): # posible error de no contener todos los atributes esperados
        #self.humidity = DHT('P3',1)
        self.samplingFrequency = atributes['samplingFrecuency']
        self.mode = atributes['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        #self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,5))
        self.dh.start()

    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                time.sleep(delay)
                result = self.humidity.read()
                self.lastHumidity = result.humidity/1.0
                self.sumHumidity += self.lastHumidity
                self.sampleCounter += 1
                gc.collect()
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
        #    data = self.sumHumidity/self.sampleCounter
        #elif self.mode == 1:
        #    data = self.lastHumidity
        #else:
        #    data = -1
        #self.sumHumidity = 0
        #self.sampleCounter = 0
        data = self.dh.getHumidity(self.mode)
        return data

    def connect(self, atributes, dh):
        self.dh = dh
        self.enabled = True
        dh.connect()
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False
        self.dh.disconnect()

    def serviceEnabled(self):
        return self.enabled
