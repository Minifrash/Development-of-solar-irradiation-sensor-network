import sys
import _thread
import time
#sys.path.append('./serviceManager')
#sys.path.append('./samplingController')
from serviceManager import ServiceManager
#from samplingController import SamplingController

class TemperatureExteriorSensor(object):

    __instance = None
    def __new__(cls): # Crear una unica instancia de la clase
        if TemperatureExteriorSensor.__instance is None: # Si no existe el atributo “instance”
            TemperatureExteriorSensor.__instance = object.__new__(cls) # lo creamos#cls.instance = super(SamplingController, cls).__new__(cls) # lo creamos
        return TemperatureExteriorSensor.__instance

    def __init__(self):
        self.serviceID = 2
        self.samplingFrequency = 0
        self.mode = 0
        self.serviceManager = ServiceManager()
        #self.samplingController = SamplingController()
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency, 1))#0 # ¿Como inicializar?


    def confService(self):
        self.samplingFrequency = self.serviceManager.getAtributeConf(serviceID, 'samplingFrequency')
        self.mode = self.serviceManager.getAtributeConf(serviceID, 'mode')

    def start(self):
        confService()
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency))

    def sampling(self, delay, id):
        while True:
            time.sleep(delay)
            self.lastTemperature = 1
            self.sumTemperature += self.lastTemperature
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
            data = self.sumTemperature/self.sampleCounter
        elif self.mode == 1:
            data = self.lastTemperature
        else:
            data = -1
        return data

    ''' Funciones Pendientes

    def connect(self):

    def disconnect(self):

    def serviceEnabled(self):

    '''
