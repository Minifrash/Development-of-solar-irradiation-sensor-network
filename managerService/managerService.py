import _thread
from samplingService.samplingService import SamplingService
from temperatureOutSensor.temperatureOutSensor import TemperatureOutSensor
from temperatureInSensor.temperatureInSensor import TemperatureInSensor
from humiditySensor.humiditySensor import HumiditySensor
from irradiationSensor.irradiationSensor import IrradiationSensor
from locationService.locationService import LocationService
from dht22Sensor.dht22Sensor import DHT22Sensor
from connectionService.connectionService import ConnectionService
from errorLogService.errorLogService import ErrorLogService

class ManagerService(object):

    def __init__(self):
        self.serviceID = 0
        self.enabled = False
        self.servicesList =  dict()
        self.sensorsList = dict()
        self.noSensorsList = dict()
        self.lock = 0
        self.dht22Sensor = DHT22Sensor()

    def confService(self):
        self.servicesList = self.readFileConf('./managerService/conf.txt')
        self.lock = _thread.allocate_lock()

    def connection(self):
	self.enabled = True
	self.confService()
	self.start()

    def disconnect(self):
	self.enabled = False
	for sensor in self.sensorsList.values():
	    sensor.disconnect()
	for service in self.noSensorsList.values():
	    service.disconnect()

    def serviceEnabled(self):
        return self.enabled

    def start(self):
        self.wakePrimaryServices()
        self.wakeAllSensorsServices()
        self.wakeAllServices()

    def wakePrimaryServices(self):
        if self.servicesList[7].get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(7)
            self.noSensorsList.setdefault(7, ConnectionService())
            self.noSensorsList.setdefault(7).connect(atributes)
        if self.servicesList[8].get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(8)
            atributes.setdefault('connectionService', self.noSensorsList.setdefault(7)) # add instance ConnectionService()
            atributes.setdefault('errorsList', self.readFileConf(atributes['descriptionsErrorsFile']))
            atributes.setdefault('warningsLits', self.readFileConf(atributes['descriptionsWarningsFile']))
            self.noSensorsList.setdefault(8, ErrorLogService())
            self.noSensorsList.setdefault(8).connect(atributes)
        if self.servicesList[2].get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(2)
	    atributes.setdefault('errorLogService', self.noSensorsList.setdefault(8))
            atributes.setdefault('connectionService', self.noSensorsList.setdefault(7)) # add instance ConnectionService()
            self.noSensorsList.setdefault(2, LocationService())
            self.noSensorsList.setdefault(2).connect(atributes)

    def wakeAllSensorsServices(self):
        for serviceID, value in self.servicesList.items():
            self.wakeSensorsServices(serviceID, value)

    def wakeSensorsServices(self, serviceID, value):
        if serviceID == 3 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('errorLogService', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, IrradiationSensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)
        if serviceID == 4 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('dht22Sensor', self.dht22Sensor)
            atributes.setdefault('errorLogService', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, TemperatureInSensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)
        if serviceID == 5 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('dht22Sensor', self.dht22Sensor)
            atributes.setdefault('errorLogService', self.noSensorsList.setdefault(8))
            self.sensorsList.setdefault(serviceID, HumiditySensor())
            self.sensorsList.setdefault(serviceID).connect(atributes)
        if serviceID == 6 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('errorLogService', self.noSensorsList.setdefault(8))
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
            atributes.setdefault('errorLogService', self.noSensorsList.setdefault(8))
            self.noSensorsList.setdefault(serviceID, SamplingService())
            self.noSensorsList.setdefault(serviceID).connect(atributes)

    def addServicesList(self, serviceID, path, serviceEnabled):
        newService = {'path': path, 'serviceEnabled': serviceEnabled}
        self.servicesList.setdefault(serviceID, newService)
        fileName = self.servicesList[self.serviceID].get('path')
        self.writeFileConf (fileName, self.servicesList)

    def deleteServiceList(self, serviceID):
	if serviceID in self.servicesList:        
	    deleteService = self.servicesList.pop(serviceID)
            fileName = self.servicesList[self.serviceID].get('path')
            self.writeFileConf (fileName, self.servicesList)
	else:
	    self.noSensorsList.setdefault(8).regError(self.serviceID, -5) #NoService Error code

    def getservicesList(self):
        return self.servicesList

    def readFileConf(self, fileName):
        dic = 0
        try:
            f = open(fileName, "r")
            dic = eval(f.read())
            f.close()
        except OSError:
	    self.noSensorsList.setdefault(8).regError(self.serviceID, -1) #OSError code
        return dic

    def writeFileConf(self, fileName, data):
        try:
            f = open(fileName, "w")
            f.write(str(data))
            f.close()
        except OSError:
	    self.noSensorsList.setdefault(8).regError(self.serviceID, -1) #OSError code

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
        fileName = self.servicesList[serviceID].get('path')
        atributes = self.readFileConf(fileName)
	if self.servicesList[serviceID].get('serviceEnabled') == 1:
	    if self.servicesList[serviceID].get('serviceSensor') == 0:
	        atributes[atribute] = value
	        self.writeFileConf(fileName, atributes)
	        self.noSensorsList[serviceID].updateAtribute(atribute, value)
	    elif self.servicesList[serviceID].get('serviceSensor') == 1:
	        atributes[atribute] = value
	        self.writeFileConf(fileName, atributes)
	        self.sensorsList[serviceID].updateAtribute(atribute, value)
	    else:# Si se solicita a un servicio que no sean los sensores o el samplingController
	        self.noSensorsList.setdefault(8).regError(self.serviceID, -8) #Incorrect Atribute Error code
	else:# Si se solicita a un servicio que no sean los sensores o el samplingController
	    self.noSensorsList.setdefault(8).regError(self.serviceID, -7) #Non-Active Service Error

    def startService(self, serviceID):
        if serviceID in self.servicesList:
            if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 0:
                 if self.servicesList[serviceID].get('serviceSensor') == 1:
		     self.servicesList[serviceID]['serviceEnabled'] = 1
                     fileName = self.servicesList[self.serviceID].get('path')
                     self.writeFileConf(fileName, self.servicesList)
                     atributes = self.getAtributesConf(serviceID)
                     self.wakeSensorsServices(serviceID, self.servicesList.setdefault(serviceID))
                     self.noSensorsList.setdefault(1).updateAtribute('servicesList', self.sensorsList)
                 elif self.servicesList[serviceID].get('serviceSensor') == 0:
		     self.servicesList[serviceID]['serviceEnabled'] = 1
                     fileName = self.servicesList[self.serviceID].get('path')
                     self.writeFileConf(fileName, self.servicesList)
                     atributes = self.getAtributesConf(serviceID)
                     self.wakeServices(serviceID, self.servicesList.setdefault(serviceID))
                 else:
                     self.noSensorsList.setdefault(8).regError(self.serviceID, -9) #Incorrect AtributeValue Error
            else:
                self.noSensorsList.setdefault(8).regError(self.serviceID, -6) #Active Service Error code
        else:
            self.noSensorsList.setdefault(8).regError(self.serviceID, -5) #NoService Error code

    def stopService(self, serviceID):
        if serviceID in self.servicesList:
             if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 1:
                 if self.servicesList[serviceID].get('serviceSensor') == 1:
		     self.servicesList[serviceID]['serviceEnabled'] = 0
                     fileName = self.servicesList[self.serviceID].get('path')
                     self.writeFileConf(fileName, self.servicesList)
                     self.sensorsList[serviceID].disconnect()
                     self.sensorsList.pop(serviceID)
                     self.noSensorsList.setdefault(1).updateAtribute('servicesList', self.sensorsList)
                 elif self.servicesList[serviceID].get('serviceSensor') == 0:
		     self.servicesList[serviceID]['serviceEnabled'] = 0
                     fileName = self.servicesList[self.serviceID].get('path')
                     self.writeFileConf(fileName, self.servicesList)
                     self.noSensorsList[serviceID].disconnect()
                     self.noSensorsList.pop(serviceID)
		 else:
                     self.noSensorsList.setdefault(8).regError(self.serviceID, -9) #Incorrect AtributeValue Error
             else:
                 self.noSensorsList.setdefault(8).regError(self.serviceID, -7) #Non-Active Service Error
        else:
            self.noSensorsList.setdefault(8).regError(self.serviceID, -5) #NoService Error code

    def restartService(self, serviceID):
        self.stopService(serviceID)
        self.startService(serviceID)
