import sys
import _thread
import time
from machine import ADC

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
        self.adc = 0 #ADC()
        #self.adc.vref(1058)
        self.panel = 0#self.adc.channel(pin='P13', attn = ADC.ATTN_11DB)

    def confService(self, atributes):
        self.adc = ADC()
        self.adc.vref(1058)
        self.panel = self.adc.channel(pin='P13', attn = ADC.ATTN_11DB)
        self.samplingFrequency = atributes['samplingFrecuency']
        self.mode = atributes['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,3))

    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                time.sleep(delay)
                self.lastRadiation = self.panel.voltage()
                self.sumRadiation += self.lastRadiation
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
            data = self.sumRadiation/self.sampleCounter
        elif self.mode == 1:
            data = self.lastRadiation
        else:
            data = -1
        self.sumRadiation = 0
        self.sampleCounter = 0
        return data

    def disconnect(self):
        self.enabled = False

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def serviceEnabled(self):
        return self.enabled
