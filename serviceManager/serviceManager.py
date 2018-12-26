import _thread
from samplingController.samplingController import SamplingController
from temperatureOutSensor.temperatureOutSensor import TemperatureOutSensor
from temperatureInSensor.temperatureInSensor import TemperatureInSensor
from humiditySensor.humiditySensor import HumiditySensor
from irradiationSensor.irradiationSensor import IrradiationSensor
from locationSensor.locationSensor import LocationSensor
from dht22.dht22 import DHT22
from connectionService.connectionService import ConnectionService
from errorLog.errorLog import ErrorLog

class ServiceManager(object):

    def __init__(self):
        self.serviceID = 0
        self.servicesList =  dict()
        self.sensorsList = dict()
        self.noSensorsList = dict()
        self.lock = 0
        self.dht = DHT22()

    def confService(self):
        self.servicesList = self.readFileConf('./serviceManager/conf.txt')
        self.lock = _thread.allocate_lock()

    def start(self):
        self.confService()
        self.wakePrimaryServices()
        self.wakeAllSensorsServices()
        self.wakeAllServices()
        self.noSensorsList.setdefault(1).sendData() # Bucle que muestrea en samplingController

    def wakePrimaryServices(self):
        if self.servicesList[7].get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(7)
            self.noSensorsList.setdefault(7, ConnectionService())
            self.noSensorsList.setdefault(7).connect(atributes)
        if self.servicesList[8].get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(8)
            atributes.setdefault('sensorsList', self.sensorsList)
            atributes.setdefault('noSensorsList', self.noSensorsList)
            atributes.setdefault('descriptionsErrors', self.readFileConf(atributes['descriptionsErrorsFile']))
            atributes.setdefault('descriptionsWarnings', self.readFileConf(atributes['descriptionsWarningsFile']))
            self.noSensorsList.setdefault(8, ErrorLog())
            self.noSensorsList.setdefault(8).connect(atributes)
        if self.servicesList[2].get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(2)
            atributes.setdefault('connectionService', self.noSensorsList.setdefault(7)) # add instance ConnectionService()
            self.noSensorsList.setdefault(2, LocationSensor())
            self.noSensorsList.setdefault(2).connect(atributes)

    def wakeAllSensorsServices(self):
        for serviceID, value in self.servicesList.items():
            self.wakeSensorsServices(serviceID, value)

    def wakeSensorsServices(self, serviceID, value):
        if serviceID == 3 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('errorLog', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, IrradiationSensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)
        if serviceID == 4 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('dht', self.dht)
            atributes.setdefault('errorLog', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, TemperatureInSensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)
        if serviceID == 5 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('dht', self.dht)
            atributes.setdefault('errorLog', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, HumiditySensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)
        if serviceID == 6 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('errorLog', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, TemperatureOutSensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)

    def wakeAllServices(self):
        for serviceID, value in self.servicesList.items():
            self.wakeServices(serviceID, value)

    def wakeServices(self, serviceID, value):
        if serviceID == 1 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('sensorsList', self.sensorsList)
            atributes.setdefault('connectionService', self.noSensorsList.setdefault(7))
            atributes.setdefault('errorLog', self.noSensorsList.setdefault(8))
            self.noSensorsList.setdefault(serviceID, SamplingController())
            self.noSensorsList.setdefault(serviceID).connect(atributes)

    def addServicesList(self, serviceID, path, serviceEnabled):
        newService = {'path': path, 'serviceEnabled':serviceEnabled}
        self.servicesList.setdefault(serviceID, newService)
        fileName = self.servicesList[self.serviceID].get('path')
        self.writeFileConf (fileName, self.servicesList)

    def deleteServiceList(self, serviceID): # Tratar posible error que devuelba pop()
        deleteService = self.servicesList.pop(serviceID)
        fileName = self.servicesList[self.serviceID].get('path')
        self.writeFileConf (fileName, self.servicesList)

    def getservicesList(self):
        return self.servicesList

    def readFileConf(self, fileName):
        dic = 0
        try:
            f = open(fileName, "r")
            dic = eval(f.read())
            f.close()
        except OSError:
	    self.noSensorsList.setdefault(8).regError(self.serviceID, -1) #IOError code
        return dic

    def writeFileConf(self, fileName, data):
        try:
            f = open(fileName, "w")
            f.write(str(data))
            f.close()
        except OSError:
	    self.noSensorsList.setdefault(8).regError(self.serviceID, -1) #IOError code

    def getAtributesConf(self, serviceID):
        fileName = self.servicesList[serviceID].get('path')
        atributes = self.readFileConf(fileName)
        return atributes

    def getAtributeConf(self, serviceID, atribute):
        fileName = self.servicesList[serviceID].get('path')
        atributes = self.readFileConf(fileName)
        value = atributes[atribute]
        return value

    def updateAtributeConf(self, serviceID, atribute, value):
        error = False
        fileName = self.servicesList[serviceID].get('path')
        atributes = self.readFileConf(fileName)
        atributes[atribute] = value
        self.writeFileConf(fileName, atributes)
        # Llamar al metodo del servicio correspondiente para que actualice su parametro
        if self.servicesList[serviceID].get('serviceSensor') != 1:
            self.noSensorsList[serviceID].updateAtribute(atribute, value)
        elif self.servicesList[serviceID].get('serviceSensor') == 1 and self.servicesList[serviceID].get('serviceEnabled') == 1:
            self.sensorsList[serviceID].updateAtribute(atribute, value)
        else: # Si se solicita a un servicio que no sean los sensores o el samplingController
            error = True
        return error

    def startService(self, serviceID): # ¿Tener en cuenta posible segunda lista de instancias para los servicios que no son sensores?
        if serviceID in self.servicesList:
            if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 0:
                 self.servicesList[serviceID]['serviceEnabled'] = 1
                 fileName = self.servicesList[self.serviceID].get('path')
                 self.writeFileConf(fileName, self.servicesList)
                 atributes = self.getAtributesConf(serviceID)
                 if self.servicesList[serviceID].get('serviceSensor') == 1:
                     self.wakeSensorsServices(serviceID, self.servicesList.setdefault(serviceID))
                     self.noSensorsList.setdefault(1).setSensorsList(self.sensorsList)
                     #self.noSensorsList.setdefault(8).setSensorsList(self.sensorsList)
                 elif self.servicesList[serviceID].get('serviceSensor') != 1:
                     self.wakeServices(serviceID, self.servicesList.setdefault(serviceID))
                     #self.noSensorsList.setdefault(8).setnoSensorsList(self.noSensorsList)
                 else:
                     self.noSensorsList.setdefault(8).regError(self.serviceID, -9) #Incorrect AtributeValue Error
            else:
                self.noSensorsList.setdefault(8).regError(self.serviceID, -6) #Active Service Error code
        else:
            self.noSensorsList.setdefault(8).regError(self.serviceID, -5) #NoService Error code

    def stopService(self, serviceID):
        if serviceID in self.servicesList:
             if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 1:
                 self.servicesList[serviceID]['serviceEnabled'] = 0
                 fileName = self.servicesList[self.serviceID].get('path')
                 self.writeFileConf(fileName, self.servicesList)
                 if self.servicesList[serviceID].get('serviceSensor') == 1:
                     self.sensorsList[serviceID].disconnect()
                     self.sensorsList.pop(serviceID)
                     self.noSensorsList.setdefault(1).setSensorsList(self.sensorsList)
                     #self.noSensorsList.setdefault(8).setSensorsList(self.sensorsList)
                 elif self.servicesList[serviceID].get('serviceSensor') != 1:
                     self.noSensorsList[serviceID].disconnect()
                     self.noSensorsList.pop(serviceID)
                     #self.noSensorsList.setdefault(8).setnoSensorsList(self.noSensorsList)
             else:
                 self.noSensorsList.setdefault(8).regError(self.serviceID, -7) #Non-Active Service Error
        else:
            self.noSensorsList.setdefault(8).regError(self.serviceID, -5) #NoService Error code

    def restartService(self, serviceID):
        self.stopService(serviceID)
        self.startService(serviceID)
