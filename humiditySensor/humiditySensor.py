import sys
import _thread
import time
#import gc

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
        self.humidity = 0
        self.dht = 0
        self.lock = 0
        self.error = 0

    def confService(self, atributes): # posible error de no contener todos los atributes esperados
        self.lock = atributes['lock']
        #print(self.lock)
        self.dht = atributes['dht']
        self.samplingFrequency = atributes['samplingFrequency']
        if not str(self.samplingFrequency).isdigit() or self.samplingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error
        self.mode = atributes['mode']
        if not str(self.mode).isdigit() or self.mode < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error

    def start(self):
        self.dht.connect(self.serviceID, self.samplingFrequency, self.lock)

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
        return error

    def getData(self):
        data = self.dht.getHumidity(self.mode)
        return data

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False
        self.dht.disconnect(self.serviceID)

    def serviceEnabled(self):
        return self.enabled
