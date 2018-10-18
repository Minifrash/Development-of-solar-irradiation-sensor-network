import sys
#sys.path.append('./samplingController')
#sys.path.append('./TemperatureOutSensor')
from samplingController.samplingController import SamplingController
from temperatureOutSensor.temperatureOutSensor import TemperatureOutSensor
from temperatureInSensor.temperatureInSensor import TemperatureInSensor
from humiditySensor.humiditySensor import HumiditySensor
from irradiationSensor.irradiationSensor import IrradiationSensor

class ServiceManager(object):

    def __init__(self):
        self.serviceID = 0 # Faltaria indicar el serviceID de ServicesManager
        self.servicesList =  dict() #self.readFileConf('./serviceManager/conf.txt')
        self.sensorsList = dict()

        self.samplingController = 0 #SamplingController()
        #self.locationSensor = 0 #LocationSensor()
        self.irradiationSensor = 0 #IrradiationSensor()
        self.temperatureInSensor = 0 #TemperatureInSensor()
        self.humiditySensor = 0 #HumiditySensor()
        self.temperatureOutSensor = 0 #TemperatureOutSensor()

    def start(self):
        self.servicesList = self.readFileConf('./serviceManager/conf.txt')
        self.confAllServices()
        self.wakeAllServices()
        self.samplingController.sendData()

    def wakeAllServices(self):  # TERMINAR
        error = 0
        for serviceID, value in self.servicesList.items():
            if serviceID == 1 and value.get('serviceEnabled') == 1:
                self.samplingController.start(self.sensorsList)
            #elif serviceID == 2 and value.get('serviceEnabled') == 1:
            #    self.locationSensor.start()
            elif serviceID == 3 and value.get('serviceEnabled') == 1:
                self.irradiationSensor.start()
            elif serviceID == 4 and value.get('serviceEnabled') == 1:
                self.temperatureInSensor.start()
            elif serviceID == 5 and value.get('serviceEnabled') == 1:
                self.humiditySensor.start()
            elif serviceID == 6 and value.get('serviceEnabled') == 1:
                self.temperatureOutSensor.start()
            else:
                error = -1
        return error

    def confAllServices(self):  # TERMINAR
        error = 0
        for serviceID, value in self.servicesList.items():
            if serviceID == 1 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.samplingController = SamplingController()
                self.samplingController.confService(atributes)
            elif serviceID == 3 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.irradiationSensor = IrradiationSensor()
                if value.get('serviceSensor') == 1:
                    self.sensorsList.setdefault(serviceID, self.irradiationSensor)
                self.irradiationSensor.confService(atributes)
            elif serviceID == 4 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.temperatureInSensor = TemperatureInSensor()
                if value.get('serviceSensor') == 1:
                    self.sensorsList.setdefault(serviceID, self.temperatureInSensor)
                self.temperatureInSensor.confService(atributes)
            elif serviceID == 5 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.humiditySensor = HumiditySensor()
                if value.get('serviceSensor') == 1:
                    self.sensorsList.setdefault(serviceID, self.humiditySensor)
                self.humiditySensor.confService(atributes)
            elif serviceID == 6 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.temperatureOutSensor = TemperatureOutSensor()
                if value.get('serviceSensor') == 1:
                    self.sensorsList.setdefault(serviceID, self.temperatureOutSensor)
                self.temperatureOutSensor.confService(atributes)
            else:
                error = -1
        return error

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

    def readFileConf (self, fileName):
        #try
        f = open(fileName, "r")
        dic = eval(f.read())
        f.close()
        #except IOError:
        error = -1 #-1 es un ejemplo, dependerá de la política de errores
        return dic

    # REPASAR ¿Como se refleja un posible error?
    def writeFileConf (self, fileName, data):
        error = 0
        #try:
        f = open(fileName, "w")
        f.write(str(data))
        f.close()
        #except IOError:
        error = -1 #-1 es un ejemplo, dependeráos.uname() de la política de errores
        return error

    def getAtributesConf(self, serviceID):
        fileName = self.servicesList[serviceID].get('path')
        atributos = self.readFileConf(fileName)
        return atributos

    def updateAtributeConf(self, serviceID, atribute, value): #Faltaria decir al service que actualice su parametro
        error = False
        fileName = self.servicesList[serviceID].get('path')  #Implementar diccionario con clave = serviceID y valor = fileNameConf
        atributes = self.readFileConf(fileName)
        atributes[atribute] = value
        self.writeFileConf(fileName, atributes)
        # Llamar al metodo del servicio correspondiente para que actualice su parametro
        return error


    '''  Funciones pendientes

    def updateFileNameService(self, serviceID, fileName)  #¿Para que se usa?

    def startService(self, serviceID)

    def stopService(self, serviceID)

    def restartService(self, serviceID)

    '''
    '''  ¿Funciones necesarias?
    # ¿Haria falta?
    def getAtributeConf(self, serviceID, atribute):
        fileName = self.servicesList[serviceID].get('path')
        atributos = self.readFileConf(fileName)
        value = atributos[atribute]
        return value
    '''


def main():
    sm = ServiceManager()
    sm.start()


main()
