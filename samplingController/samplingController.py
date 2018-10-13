import sys
sys.path.append('./serviceManager')
from serviceManager import ServiceManager


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
        #self.temperatureExteriorSensor = TemperatureExteriorSensor()
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


''' Funciones pendientes
    def sleep(self):

    def wakeUp(self):

    def sendData(self):

    def addServicesList(self, serviceID)  ¿Haria falta?
 '''

def main():
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

main()
