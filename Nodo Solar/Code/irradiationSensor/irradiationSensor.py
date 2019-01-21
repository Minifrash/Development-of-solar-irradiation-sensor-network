import _thread
import time
from machine import Pin, ADC, DAC
from libraries.memoryManager import *

class IrradiationSensor(object):

    def __init__(self):
        self.serviceID = 3
        self.samplingFrequency = 0
        self.mode = 0
        self.lastRadiation = 0
        self.sumRadiation = 0
        self.sampleCounter = 0
        self.enabled = False
        self.sampleThread = 0
        self.powerPin = 0
        self.adc = 0
        self.panel = 0
        self.vBiasDAC = 0
        self.lock = 0
        self.errorLogService = 0
        self.erCounter = 3

    def confService(self, atributes):
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.adc = ADC()
        self.adc.vref(1058)
        self.vBiasDAC = DAC('P22')
        self.vBiasDAC.write(0.135) # approximately 0.5 V
        self.panel = self.adc.channel(pin='P13', attn = ADC.ATTN_11DB)
        self.errorLogService = atributes['errorLogService']
        self.lock = atributes['lock']
        if ('mode' in atributes) and ('samplingFrequency' in atributes):
            if not str(atributes['samplingFrequency']).isdigit() or atributes['samplingFrequency'] < 0: #Comprobar si es un numero (isdigit) y si es negativo
                self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
            else:
                self.samplingFrequency = atributes['samplingFrequency']
            if not str(atributes['mode']).isdigit() or atributes['mode'] < 0: #Comprobar si es un numero (isdigit) y si es negativo
                self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
            else:
                self.mode = atributes['mode']
        else:
            self.errorLogService.regError(self.serviceID, -2) #ConfFile Error

    def start(self):
        try:
            self.sampleThread = _thread.start_new_thread(self.sampling, ())
        except:
            self.errorLogService.regError(self.serviceID, -3) #CreateThread Error code

    def sampling(self):
        while True:
            if self.enabled is True:
                time.sleep(self.samplingFrequency-0.002) # Reducir el tiempo de muestreo teniendo en cuenta el sleep de powerPin
                self.lock.acquire()
                self.powerPin(1)
                time.sleep(0.002)
                self.lastRadiation = self.panel.voltage()
                count = 0
                #El valor para el panel es aproximado pues se considera que devuelve 1000 en un día soleado de 25º
                while((self.lastRadiation < 1.0 or self.lastRadiation > 10000.0) and count < self.erCounter):
                    time.sleep(0.002)
                    self.lastRadiation = self.panel.voltage()
                    count += 1
                if (self.lastRadiation < 1.0 or self.lastRadiation > 10000.0):
                    self.errorLogService.regError(self.serviceID, -11) #Incorrect Value Error code
                else:
                    self.sumRadiation += self.lastRadiation
                    self.sampleCounter += 1
                collectMemory()
                self.powerPin(0)
                self.lock.release()
            else:
                _thread.exit()

    def updateAtribute(self, atribute, newValue):
        if not str(newValue).isdigit() or newValue < 0:
            self.errorLogService.regError(self.serviceID, -9) #Incorrect Atribute Error
        else:
            if atribute == 'samplingFrequency':
                self.samplingFrequency = newValue
            elif atribute == 'mode':
                self.mode = newValue
            else:
                self.errorLogService.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def getData(self):
        data = 0
        self.lock.acquire()
        if self.mode == 0:
            try:
                data = self.sumRadiation/self.sampleCounter
            except ZeroDivisionError:
                self.errorLogService.regError(self.serviceID, -10) #ZeroDivisionError code
        elif self.mode == 1:
            data = self.lastRadiation
        else:
            self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        self.sumRadiation = 0
        self.sampleCounter = 0
        self.lock.release()
        return data

    def disconnect(self):
        self.enabled = False

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def serviceEnabled(self):
        return self.enabled
