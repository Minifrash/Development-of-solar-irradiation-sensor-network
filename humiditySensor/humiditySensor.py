import sys
import _thread
import time
import gc
from humiditySensor.dht import DHT

class HumiditySensor(object):

    def __init__(self):
        self.serviceID = 5
        self.samplingFrequency = 0
        self.mode = 0
        self.lastHumidity = 0
        self.sumHumidity = 0
        self.sampleCounter = 0
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = 0 #_thread.start_new_thread(self.sampling, (self.samplingFrequency, 1))#0 # ¿Como inicializar?
        self.close = False
        self.humidity = DHT('P3',1)

    def confService(self, atributos):
        self.samplingFrequency = atributos['samplingFrecuency']
        self.mode = atributos['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,5))

    def sampling(self, delay, id):
        while True:
            if self.close is True:
                _thread.exit()
            time.sleep(delay)
            result = self.humidity.read()
            self.lastHumidity = result.humidity/1.0
            self.sumHumidity += self.lastHumidity
            self.sampleCounter += 1
            gc.collect()

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
            data = self.sumHumidity/self.sampleCounter
        elif self.mode == 1:
            data = self.lastHumidity
        else:
            data = -1
        self.sumHumidity = 0
        self.sampleCounter = 0
        return data

    def disconnect(self):
        self.close = True

    ''' Funciones Pendientes

    def connect(self):

    def serviceEnabled(self):
        return enabled
    '''
