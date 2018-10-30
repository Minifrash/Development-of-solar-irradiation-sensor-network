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
        self.error = 0
        self.erCounter = 3

    def confService(self, atributes):
        self.adc = ADC()
        self.adc.vref(1058)
        self.panel = self.adc.channel(pin='P13', attn = ADC.ATTN_11DB)
        self.samplingFrequency = atributes['samplingFrecuency']
        if not self.samplingFrequency.isdigit() or self.samplingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error
        self.mode = atributes['mode']
        if not self.mode.isdigit() or self.mode < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.error = -9 #Incorrect AtributeValue Error

    def start(self):
        # Crear el thread para la funcion sendData()
        error = 0
        try:
            self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,3))
        except:
            error = -3 #CreateThread Error code
            #self.error = -3
        return error

    def sampling(self, delay, id):
        while True:
            if self.enabled is True:
                time.sleep(delay)
                self.lastRadiation = self.panel.voltage()
                count = 0
                #El valor para el panel es aproximado pues se considera que devuelve 1000 en un día soleado de 25º
                while((self.lastRadiation < 1.0 or self.lastRadiation > 1200.0) and count < self.erCounter):
                    self.lastRadiation = self.panel.voltage()
                    count += 1
                count = 0
                if (self.lastRadiation < 1.0 or self.lastRadiation > 1200.0): #Si a la salida del bucle sigue siendo una mala muestra, se pasa a self.error
                    self.error = -11 #Incorrect Value Error code
                else:
                self.sumRadiation += self.lastRadiation
                self.sampleCounter += 1
            else:
                try:
                    _thread.exit()
                except SystemExit:
                    self.error = -4 #SystemExit code

    def updateAtribute(self, atribute, newValue):
        error = 0
        if not newValue.isdigit() or newValue < 0: #¿Lo hace serviceManager?
            self.error = -9 #Incorrect AtributeValue Error
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            error = -8 # error de atributo incorrecto
            #self.error = -8 #Incorrect Atribute Error code
        return error


    def getData(self):
        data = -1 # Posible error
        if self.mode == 0:
            try:
                data = self.sumRadiation/self.sampleCounter
            except ZeroDivisionError:
                self.error = -10 #ZeroDivisionError code
        elif self.mode == 1:
            data = self.lastRadiation
        else:
            data = -9
            #self.error = -9 #Incorrect AtributeValue Error
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
