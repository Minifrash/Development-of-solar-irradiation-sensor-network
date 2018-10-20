import sys
import _thread
import time
#from temperatureInSensor.dht import DHT

class TemperatureInSensor(object):

    def __init__(self):
        self.serviceID = 4
        self.samplingFrequency = 0
        self.mode = 0
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.enabled = True
        self.sampleThread = 0
        #self.temp = DHT('P3',1)

    def confService(self, atributos):
        self.samplingFrequency = atributos['samplingFrecuency']
        self.mode = atributos['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,4))

    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                time.sleep(delay)
                result = 2#self.temp.read()
                self.lastTemperature = result#result.temperature/1.0
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
        self.enabled = False

    def connect(self):
        self.enabled = True
        self.start()

    def serviceEnabled(self):
        return self.enabled
