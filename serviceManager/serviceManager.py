import sys
#sys.path.append('./samplingController')
#sys.path.append('./TemperatureOutSensor')
from samplingController.samplingController import SamplingController
from temperatureOutSensor.temperatureOutSensor import TemperatureOutSensor

class ServiceManager(object):

    def __init__(self):
        self.serviceID = 0 # Faltaria indicar el serviceID de ServicesManager
        self.servicesList =  dict() #self.readFileConf('./serviceManager/conf.txt')
        self.sensorsList = dict()

        self.samplingController = 0 #SamplingController()
        #self.locationSensor = LocationSensor()
        #self.irradiationSensor = IrradiationSensor()
        #self.temperatureInteriorSensor = TemperatureInteriorSensor()
        #self.humiditySensor = HumiditySensor()
        self.TemperatureOutSensor = 0 #TemperatureOutSensor()

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
            elif serviceID == 2 and value.get('serviceEnabled') == 1:
                self.TemperatureOutSensor.start()
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
            elif serviceID == 2 and value.get('serviceEnabled') == 1:
                atributes = self.getAtributesConf(serviceID)
                self.TemperatureOutSensor = TemperatureOutSensor()
                if value.get('serviceSensor') == 1:
                    self.sensorsList.setdefault(serviceID, self.TemperatureOutSensor)
                self.TemperatureOutSensor.confService(atributes)
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
        f = open(fileName, "r")
        dic = eval(f.read())
        f.close()
        return dic

    # REPASAR ¿Como se refleja un posible error?
    def writeFileConf (self, fileName, data):
        error = False
        f = open(fileName, "w")
        f.write(str(data))
        f.close()
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
    '''
    sm = ServiceManager()
    services = sm.getservicesList()

    print('Lista de servicios:')
    print(services.items())
    print('Lista de servicios con nuevo servicio 5:')
    services = sm.addServicesList(5, './prueba/conf.txt', 0)
    print(services.items())
    print('Lista de servicios sin servicio 5:')
    services = sm.deleteServiceList(5)
    print(services.items())


    print('Atributo sleepTime del servicio 1:')
    atribute = sm.getAtributeConf(1, 'sleepTime')
    print(atribute)

    sm.updateAtributeConf(1, 'sleepTime', atribute+1)
    print('Atributo actualizado sleepTime del servicio 1:')
    atribute = sm.getAtributeConf(1, 'sleepTime')
    print(atribute)
    '''
    sm = ServiceManager()
    sm.start()


main()
