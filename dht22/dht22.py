import sys
import _thread
import time
import gc
from libraries.dht import DHT
#import random

class DHT22(object):

    def __init__(self):
        self.enabledHumidity = False
        self.lastHumidity = 0
        self.sumHumidity = 0
        self.sampleCounterHumidity = 0
        self.enabledTemperature = False
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounterTemperature = 0
        self.samplingFrequency = 1
        self.sampleThread = 0
        self.dht = 0
        self.lock = 0
        self.enabled = False
        self.error = 0 #Codigo de error o cero si todo bien
        self.erCounter = 3 #Contador para reintentos tras error

    def conf(self, samplingFrequency):
        self.samplingFrequency = samplingFrequency
        self.dht = DHT('P3',1)

    def start(self):
        error = 0
        if self.sampleThread == 0:
            try:
                self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,5))
            except:
                error = -3 #CreateThread Error code
                #self.error = -3
        #else error hilo ya iniciado?
        return error

    def sampling(self, delay, id):
        while True:
            if self.enabled == True:
                result = self.dht.read()
                self.lock.acquire()
                #result = self.dht.read()
                if self.enabledHumidity is True:
                    #print("H")
                    #print(result.humidity)
                    self.lastHumidity = result.humidity/1.0
                    self.sumHumidity += self.lastHumidity
                    self.sampleCounterHumidity += 1
                if self.enabledTemperature is True:
                    #print("T")
                    #print(result.temperature)
                    self.lastTemperature = result.temperature/1.0
                    self.sumTemperature += self.lastTemperature
                    self.sampleCounterTemperature += 1
                gc.collect()
                self.lock.release()
                time.sleep(delay)
            else:
                try:
                    _thread.exit()
                except SystemExit:
                    self.error = -4 #SystemExit code


    def getHumidity(self, mode):
        data = -1 # Posible error
        self.lock.acquire()
        if self.enabledHumidity is True:
            if mode == 0:
                try:
                    data = self.sumHumidity/self.sampleCounterHumidity
                except ZeroDivisionError:
                    error = -10
                    #self.error = -10 #ZeroDivisionError code
            elif mode == 1:
                data = self.lastHumidity
            else:
                data = -9
                #self.error = -9 #Incorrect AtributeValue Error
            self.sumHumidity = 0
            self.sampleCounterHumidity = 0
        else:
            error = -1 #Servicio desconectado
        self.lock.release()
        return data

    def getTemperature(self, mode):
        data = -1 # Posible error
        self.lock.acquire()
        if self.enabledTemperature is True:
            if mode == 0:
                try:
                    data = self.sumTemperature/self.sampleCounterTemperature
                except ZeroDivisionError:
                    error = -10
                    #self.error = -10 #ZeroDivisionError code
            elif mode == 1:
                data = self.lastTemperature
            else:
                data = -9
                #self.error = -9 #Incorrect AtributeValue Error
            self.sumTemperature = 0
            self.sampleCounterTemperature = 0
        else:
            error = -1 #Servicio desconectado
        self.lock.release()
        return data


    def connect(self, serviceID, samplingFrequency, lock):
        error = 0
        if serviceID == 4 and self.enabledTemperature is False:
            self.enabledTemperature = True
        elif serviceID == 5 and self.enabledHumidity is False:
            self.enabledHumidity = True
        else:
            error = -6 #Fallo en el serviceID o ya esta conectado #Active Service Error

        if self.enabled is False:
            self.enabled = True
            self.lock = lock
            print(self.lock)
            self.conf(samplingFrequency)
            self.start()
        return error

    def disconnect(self, serviceID):
        if serviceID == 4 and self.enabledTemperature == True:
            self.enabledTemperature = False
        elif serviceID == 5 and self.enabledHumidity == True:
            self.enabledHumidity = False
        else:
            error = -7 #Fallo en el serviceID o ya esta conectado #Non-Active Service Error

        if self.enabledTemperature == False and self.enabledHumidity == False:
            self.sampleThread = 0
            self.enabled = False
