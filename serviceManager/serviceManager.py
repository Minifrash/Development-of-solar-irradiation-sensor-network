import sys
import _thread
#sys.path.append('./samplingController')
#sys.path.append('./temperatureOutSensor')
#sys.path.append('./temperatureInSensor')
#sys.path.append('./humiditySensor')
#sys.path.append('./irradiationSensor')
#sys.path.append('./dht22')

#from samplingController import SamplingController
#from temperatureOutSensor import TemperatureOutSensor
#from temperatureInSensor import TemperatureInSensor
#from humiditySensor import HumiditySensor
#from irradiationSensor import IrradiationSensor
#from dht22 import DHT22

from samplingController.samplingController import SamplingController
from temperatureOutSensor.temperatureOutSensor import TemperatureOutSensor
from temperatureInSensor.temperatureInSensor import TemperatureInSensor
from humiditySensor.humiditySensor import HumiditySensor
from irradiationSensor.irradiationSensor import IrradiationSensor
#from locationSensor.locationSensor import LocationSensor
from dht22.dht22 import DHT22


class ServiceManager(object):

    def __init__(self):
        self.serviceID = 0
        self.servicesList =  dict()
        self.sensorsList = dict()
        self.NoSensorsServicesList = dict()
        self.lock = 0
        self.error = 0
        self.samplingController = SamplingController()
        #self.locationSensor = LocationSensor()
        self.irradiationSensor = IrradiationSensor()
        self.temperatureInSensor = TemperatureInSensor()
        self.humiditySensor = HumiditySensor()
        self.temperatureOutSensor = TemperatureOutSensor()
        self.dht = DHT22()

    def confService(self):
        self.servicesList = self.readFileConf('./serviceManager/conf.txt')
        self.lock = _thread.allocate_lock()

    def start(self):
        self.confService()
        self.wakeAllSensorsServices()
        self.wakeAllServices()
        self.samplingController.sendData()

    def wakeAllServices(self):
        for serviceID, value in self.servicesList.items():
            self.wakeServices(serviceID, value)

    def wakeServices(self, serviceID, value):
        if serviceID == 1 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('sensorsList', self.sensorsList)
            self.NoSensorsServicesList.setdefault(serviceID, self.samplingController)
            self.samplingController.connect(atributes)

    def wakeAllSensorsServices(self):
        error = 0
        for serviceID, value in self.servicesList.items():
            self.wakeSensorsServices(serviceID, value)
        return error

    def wakeSensorsServices(self, serviceID, value):
        #if serviceID == 2 and value.get('serviceEnabled') == 1:
        #    atributes = self.getAtributesConf(serviceID)
        #    self.sensorsList.setdefault(serviceID, self.locationSensor)
        #    self.locationSensor.connect(atributes, self.lock)
        if serviceID == 3 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            self.sensorsList.setdefault(serviceID, self.irradiationSensor)
            self.irradiationSensor.connect(atributes)
        if serviceID == 4 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('dht', self.dht)
            self.sensorsList.setdefault(serviceID, self.temperatureInSensor)
            self.temperatureInSensor.connect(atributes)
        if serviceID == 5 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            atributes.setdefault('dht', self.dht)
            self.sensorsList.setdefault(serviceID, self.humiditySensor)
            self.humiditySensor.connect(atributes)
        if serviceID == 6 and value.get('serviceEnabled') == 1:
            atributes = self.getAtributesConf(serviceID)
            atributes.setdefault('lock', self.lock)
            self.sensorsList.setdefault(serviceID, self.temperatureOutSensor)
            self.temperatureOutSensor.connect(atributes)

    def addServicesList(self, serviceID, path, serviceEnabled):
        newService = {'path': path, 'serviceEnabled':serviceEnabled}
        self.servicesList.setdefault(serviceID, newService)
        fileName = self.servicesList[self.serviceID].get('path')
        self.writeFileConf (fileName, self.servicesList)
        return self.servicesList

    def deleteServiceList(self, serviceID): # Tratar posible error que devuelba pop()
        deleteService = self.servicesList.pop(serviceID)
        fileName = self.servicesList[self.serviceID].get('path')
        self.writeFileConf (fileName, self.servicesList)
        return self.servicesList

    def getservicesList(self):
        return self.servicesList

    def readFileConf(self, fileName):
        dic = 0
        try:
            f = open(fileName, "r")
            dic = eval(f.read())
            f.close()
        except IOError:
            dic = -1
            #self.error = -1 #IOError code
        return dic

    # REPASAR ¿Como se refleja un posible error?
    def writeFileConf(self, fileName, data):
        error = 0
        try:
            f = open(fileName, "w")
            f.write(str(data))
            f.close()
        except IOError:
            error = -1
            #self.error = -1 #IOError code
        return error #delvolver self.error?

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
            self.NoSensorsServicesList[serviceID].updateAtribute(atribute, value)
        elif self.servicesList[serviceID].get('serviceSensor') == 1 and self.servicesList[serviceID].get('serviceEnabled') == 1:
            self.sensorsList[serviceID].updateAtribute(atribute, value)
        else: # Si se solicita a un servicio que no sean los sensores o el samplingController
            error = True
        return error

    def startService(self, serviceID): # ¿Tener en cuenta posible segunda lista de instancias para los servicios que no son sensores?
        error = 0
        if serviceID in self.servicesList:
            if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 0:
                 self.servicesList[serviceID]['serviceEnabled'] = 1
                 fileName = self.servicesList[self.serviceID].get('path')
                 self.writeFileConf(fileName, self.servicesList)
                 atributes = self.getAtributesConf(serviceID)
                 if self.servicesList[serviceID].get('serviceSensor') == 1:
                     self.wakeSensorsServices(serviceID, self.servicesList.setdefault(serviceID))
                 elif self.servicesList[serviceID].get('serviceSensor') != 1:
                     self.wakeServices(serviceID, self.servicesList.setdefault(serviceID))
                 else:
                    error = -9 #Incorrect AtributeValue Error
                    self.error = -9
            else:
                 error = -6
                 self.error = -6 #Active Service Error code
        else:
            error = -5
            self.error = -5 #NoService Error code
        return error

    def stopService(self, serviceID):
        error = 0
        if serviceID in self.servicesList:
             if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 1:
                 self.servicesList[serviceID]['serviceEnabled'] = 0
                 fileName = self.servicesList[self.serviceID].get('path')
                 self.writeFileConf(fileName, self.servicesList)
                 if self.servicesList[serviceID].get('serviceSensor') == 1:
                     self.sensorsList[serviceID].disconnect()
                     self.sensorsList.pop(serviceID)
                 elif self.servicesList[serviceID].get('serviceSensor') != 1:
                    #self.NoSensorsServicesList[serviceID].disconnect()
                    self.NoSensorsServicesList.pop(serviceID)
             else:
                 error = -7
                 self.error = -7 #Non-Active Service Error
        else:
            error = -5
            self.error = -5 #NoService Error code
        return error

    def restartService(self, serviceID): # REVISAR
        self.stopService(serviceID)
        self.startService(serviceID)


def main():
    sm = ServiceManager()
    #sm.confService()
    #sm.startService(1)
    #sm.startService(3)
    #sm.startService(4)
    #sm.startService(5)
    #sm.startService(6)
    sm.start()
    #sm.stopService(3)
    #sm.stopService(4)
    #sm.stopService(5)
    #sm.stopService(6)
    #sm.stopService(1)


main()
