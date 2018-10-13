from serviceManager.serviceManager import ServicesManager
from temperatureExteriorSensor.temperatureExteriorSensor import TemperatureExteriorSensor

class SamplingController(object):
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

    def updateAtribute(self, atribute, newValue):
        if atribute == 'servicesList':
            self.servicesList = newValue
        elif atribute == 'sendingFrequency':
            self.sendingFrequency = newValue
        elif atribute == 'samplingFrequency': # ¿Haria falta?
            self.sendingFrequency = newValue # ¿Haria falta?
        elif atribute == 'sleepTime':
            self.sleepTime = newValue
        elif atribute == 'wakeTime'
            self.wakeTime = newValue
        else:
            # error de atributo incorrecto

    #Tratar posibles errores
    def confService():
        self.servicesList = self.serviceManager.getservicesList()
        self.sendingFrequency = self.serviceManager.getAtributeConf(serviceID, 'sendingFrequency')
        self.samplingFrequency = self.serviceManager.getAtributeConf(serviceID, 'samplingFrequency') # ¿Haria falta?
        self.sleepTime = self.serviceManager.getAtributeConf(serviceID, 'sleepTime')
        self.wakeTime = self.serviceManager.getAtributeConf(serviceID, 'wakeTime')

    def start():
        confService()
        self.serviceManager.wakeAllServices()
        # Crear el thread para la funcion sendData()

    ''' Funciones que faltan  '''
    #def dleep():

    #def wakeUp():

    #def sendData():


def main():
    sc = SamplingController()
