import sys
import _thread
import time
#from libraries.dht import DHT

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

    def confService(self, atributes, dht):
        #self.temp = DHT('P3',1)
        self.dht = dht
        self.samplingFrequency = atributes['samplingFrecuency']
        self.mode = atributes['mode']

    def start(self):
        self.dht.connect(self.serviceID, self.samplingFrequency)
        #self.dht.start()

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
        data = self.dht.getTemperature(self.mode)
        return data

    def connect(self, atributes, dht):
        self.enabled = True
        self.confService(atributes, dht)
        self.start()

    def disconnect(self):
        self.enabled = False
        self.dht.disconnect(self.serviceID)

    def serviceEnabled(self):
        return self.enabled
