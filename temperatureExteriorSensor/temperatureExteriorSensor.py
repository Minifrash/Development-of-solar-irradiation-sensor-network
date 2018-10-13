import sys
sys.path.append('./serviceManager')
sys.path.append('./samplingController')
from serviceManager import ServiceManager
from samplingController import SamplingController


class TemperatureExteriorSensor(object):

    def __init__(self):
        self.serviceID = 2
        self.samplingFrequency = 0
        self.mode = 0
        self.serviceManager = ServiceManager()
        self.samplingController = SamplingController()
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = 0 # ¿Como inicializar?


    def confService(self):
        self.samplingFrequency = self.serviceManager.getAtributeConf(serviceID, 'samplingFrequency')
        self.mode = self.serviceManager.getAtributeConf(serviceID, 'mode')

    def start(self):
        confService()
        # Crear el thread para la funcion sendData()

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
        if self.modo == 0:
            data = self.sumTemperature/self.sampleCounter
        else self.mode == 1:
            data = self.lastTemperature
        return data

    ''' Funciones Pendientes
    def sampling(self):

    def connect(self):

    def disconnect(self):

    def serviceEnabled(self):

    '''
