#import _thread
import time
import sys
sys.path.append('./temperatureExteriorSensor')
sys.path.append('./serviceManager')
from serviceManager import ServiceManager



class SamplingController(object):

    __instance = None
    def __new__(cls): # Crear una unica instancia de la clase
        if SamplingController.__instance is None: # Si no existe el atributo “instance”
            SamplingController.__instance = object.__new__(cls) # lo creamos#cls.instance = super(SamplingController, cls).__new__(cls) # lo creamos
        return SamplingController.__instance

    '''
    def __new__(cls): # Crear una unica instancia de la clase
        if not hasattr(cls, 'instance'): # Si no existe el atributo “instance”
            cls.instance = object.__new__(cls) # lo creamos#cls.instance = super(SamplingController, cls).__new__(cls) # lo creamos
        return cls.instance
    '''

    def __init__(self):
        self.serviceID = 1 # Faltaria indicar el serviceID de ServicesManager
        self.servicesList = dict()
        self.sendingFrequency = 0
        self.samplingFrequency = 0 # ¿Haria falta?
        self.sleepTime = 0
        self.wakeTime = 0
        self.serviceManager = ServiceManager()
        #self.locationSensor = LocationSensor()
        #self.irradiationSensor = IrradiationSensor()
        #self.temperatureInteriorSensor = TemperatureInteriorSensor()
        #self.humiditySensor = HumiditySensor()
        self.temperatureExteriorSensor = TemperatureExteriorSensor()
        self.sampleThread = 0 # ¿Como inicializar?

    #Tratar posibles errores
    def confService(self):
        self.servicesList = self.serviceManager.getservicesList()
        self.sendingFrequency = self.serviceManager.getAtributeConf(self.serviceID, 'sendingFrequency')
        self.samplingFrequency = self.serviceManager.getAtributeConf(self.serviceID, 'samplingFrecuency') # ¿Haria falta?
        self.sleepTime = self.serviceManager.getAtributeConf(self.serviceID, 'sleepTime')
        self.wakeTime = self.serviceManager.getAtributeConf(self.serviceID, 'wakeTime')

    def start(self):
        self.confService()
        #self.serviceManager.wakeAllServices()
        # Crear el thread para la funcion sendData()


    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'servicesList':
            self.servicesList = newValue
        elif atribute == 'sendingFrequency':
            self.sendingFrequency = newValue
        elif atribute == 'samplingFrequency': # ¿Haria falta?
            self.sendingFrequency = newValue # ¿Haria falta?
        elif atribute == 'sleepTime':
            self.sleepTime = newValue
        elif atribute == 'wakeTime':
            self.wakeTime = newValue
        else:
            error = True # error de atributo incorrecto
        return error

    def sendData(self):
        for i in range(5):
            time.sleep(5)
            print(self.temperatureExteriorSensor.getData())

''' Funciones pendientes
    def sleep(self):

    def wakeUp(self):

    def sendData(self):

    def addServicesList(self, serviceID)  ¿Haria falta?
 '''

def main():
    '''
    sc = SamplingController()
    sc.start()

    print('Lista de servicios:')
    print(sc.servicesList.items())
    print('sendingFrequency:')
    print(sc.sendingFrequency)
    print('samplingFrequency:')
    print(sc.samplingFrequency)
    print('sleepTime:')
    print(sc.sleepTime)
    print('wakeTime:')
    print(sc.wakeTime)

    sc.updateAtribute('sleepTime', sc.sleepTime+1)
    print('Actualizacion de sleepTime:')
    print(sc.sleepTime)
    '''
    '''
    sm1 = SamplingController()
    sm2 = SamplingController()

    print(sm1 is sm2)
    print('sleepTime sm1:')
    print(sm1.sleepTime)
    print('sleepTime sm2:')
    print(sm2.sleepTime)
    sm1.updateAtribute('sleepTime', sm1.sleepTime+2)
    print('sleepTime sm1:')
    print(sm1.sleepTime)
    print('sleepTime sm2:')
    print(sm2.sleepTime)
    '''
    sc = SamplingController()
    sc.start()
    sc.sendData()



main()
