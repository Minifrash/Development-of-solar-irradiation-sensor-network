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
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = 0 #_thread.start_new_thread(self.sampling, (self.samplingFrequency, 1))#0 # ¿Como inicializar?
        self.close = False
        self.adc = ADC()
        self.adc.vref(1058)
        self.panel = self.adc.channel(pin='P13', attn = ADC.ATTN_11DB)

    def confService(self, atributes):
        self.samplingFrequency = atributes['samplingFrecuency']
        self.mode = atributes['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,3))

    def sampling(self, delay, id):
        while True:
            if self.close is True:
                _thread.exit()
            time.sleep(delay)
            self.lastRadiation = self.panel.voltage()
            self.sumRadiation += self.lastRadiation
            self.sampleCounter += 1

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
        self.close = True

    ''' Funciones Pendientes

    def connect(self):

    def serviceEnabled(self):
        return enabled
    '''
