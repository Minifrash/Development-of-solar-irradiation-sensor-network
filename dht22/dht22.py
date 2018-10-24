import sys
import _thread
import time
import random

class DHT22(object):

    def __init__(self):
        self.enabled = False
        self.samplingFrequency = 1
        self.lastHumidity = 0
        self.sumHumidity = 0
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.dht = 0
        self.sampleCounterHumidity = 0
        self.sampleCounterTemperature = 0
        self.sampleThread = 0

    def start(self):
        #self.dht =  DHT('P3',1)
        if self.sampleThread == 0:
            print("OK")
            self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,5))


    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                time.sleep(delay)
                result = 2#self.humidity.read()
                self.lastHumidity = random.randrange(10)#2#result.humidity/1.0
                self.sumHumidity += self.lastHumidity
                self.lastTemperature = random.randrange(10)#3#result.temperature/1.0
                self.sumTemperature += self.lastTemperature
                self.sampleCounterTemperature += 1
                self.sampleCounterHumidity += 1
                #gc.collect()
            else:
                _thread.exit()


    def getHumidity(self, mode):
        data = -1 # Posible error
        if mode == 0:
            data = self.sumHumidity/self.sampleCounterHumidity
        elif mode == 1:
            data = self.lastHumidity
        else:
            data = -1
        self.sumHumidity = 0
        self.sampleCounterHumidity = 0
        return data

    def getTemperature(self, mode):
        data = -1 # Posible error
        if mode == 0:
            data = self.sumTemperature/self.sampleCounterTemperature
        elif mode == 1:
            data = self.lastTemperature
        else:
            data = -1
        self.sumTemperature = 0
        self.sampleCounterTemperature = 0
        return data


    def connect(self):
        if self.enabled == False:
            self.enabled = True
            #self.confService(atributes)
            self.start()

    def disconnect(self):
        self.sampleThread = 0
        self.enabled = False
