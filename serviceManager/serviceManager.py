import sys
#sys.path.append('./samplingController')
#sys.path.append('./temperatureOutSensor')
#sys.path.append('./temperatureInSensor')
#sys.path.append('./humiditySensor')
#sys.path.append('./irradiationSensor')

#from samplingController import SamplingController
#from temperatureOutSensor import TemperatureOutSensor
#from temperatureInSensor import TemperatureInSensor
#from humiditySensor import HumiditySensor
#from irradiationSensor import IrradiationSensor

from samplingController.samplingController import SamplingController
from temperatureOutSensor.temperatureOutSensor import TemperatureOutSensor
from temperatureInSensor.temperatureInSensor import TemperatureInSensor
from humiditySensor.humiditySensor import HumiditySensor
from irradiationSensor.irradiationSensor import IrradiationSensor

class ServiceManager(object):

    def __init__(self):
        self.serviceID = 0
        self.servicesList =  dict()
        self.sensorsList = dict()
        self.error = 0

        self.samplingController = SamplingController()
        #self.locationSensor = LocationSensor()
        self.irradiationSensor = IrradiationSensor()
        self.temperatureInSensor = TemperatureInSensor()
        self.humiditySensor = HumiditySensor()
        self.temperatureOutSensor = TemperatureOutSensor()

    def start(self):
        self.servicesList = self.readFileConf('./serviceManager/conf.txt')
        self.wakeAllServices()
        self.samplingController.start(self.sensorsList)
        self.samplingController.sendData()

    def wakeAllServices(self):  # ¿Posible reducir codido?
        error = 0
        for serviceID, value in self.servicesList.items():
            if serviceID == 1 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.samplingController.confService(atributes)
            elif serviceID == 3 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.sensorsList.setdefault(serviceID, self.irradiationSensor)
                self.irradiationSensor.connect(atributes)
            elif serviceID == 4 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.sensorsList.setdefault(serviceID, self.temperatureInSensor)
                self.temperatureInSensor.connect(atributes)
            elif serviceID == 5 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.sensorsList.setdefault(serviceID, self.humiditySensor)
                self.humiditySensor.connect(atributes)
            elif serviceID == 6 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.sensorsList.setdefault(serviceID, self.temperatureOutSensor)
                self.temperatureOutSensor.connect(atributes)
            else:
                error = -5
                self.error = -5 #NoService Error code
        return error #delvolver self.error?

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
            #self.error = -1 #IOError code
            dic = -1
        return dic

    # REPASAR ¿Como se refleja un posible error?
    def writeFileConf(self, fileName, data):
        error = 0
        try:
            f = open(fileName, "w")
            f.write(str(data))
            f.close()
        except IOError:
            self.error = -1 #IOError code
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
        if serviceID == 1:
            self.samplingController.updateAtribute(atribute, value)
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
                 self.sensorsList[serviceID].connect(atributes)
             else:
                 error = -1
                 self.error = -6 #Active Service Error code
        else:
            error = -1
            self.error = -5 #NoService Error code
        return error #delvolver self.error?

    def stopService(self, serviceID):
        if serviceID in self.servicesList:
             if 'serviceEnabled' in self.servicesList[serviceID] and self.servicesList[serviceID].get('serviceEnabled') == 1:
                 self.servicesList[serviceID]['serviceEnabled'] = 0
                 fileName = self.servicesList[self.serviceID].get('path')
                 self.writeFileConf(fileName, self.servicesList)
                 self.sensorsList[serviceID].disconnect()
             else:
                 error = -1
                 self.error = -7 #Non-Active Service Error
        else:
            error = -1
            self.error = -5 #NoService Error code
        return error #delvolver self.error?

    def restartService(self, serviceID): # REVISAR
        self.stopService(serviceID)
        self.startService(serviceID)

    '''  Funciones pendientes

    def updateFileNameService(self, serviceID, fileName)  #¿Para que se usa?

    '''


def main():
    sm = ServiceManager()
    sm.start()


main()
