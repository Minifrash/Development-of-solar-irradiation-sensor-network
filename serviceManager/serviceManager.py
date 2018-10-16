import sys
#sys.path.append('./samplingController')
sys.path.append('./temperatureExteriorSensor')
#from samplingController import SamplingController
#from temperatureExteriorSensor import TemperatureExteriorSensor

class ServiceManager(object):

    __instance = None
    def __new__(cls): # Crear una unica instancia de la clase
        if ServiceManager.__instance is None: # Si no existe el atributo “instance”
            ServiceManager.__instance = object.__new__(cls) # lo creamos#cls.instance = super(SamplingController, cls).__new__(cls) # lo creamos
        return ServiceManager.__instance

    def __init__(self):
        self.serviceID = 0 # Faltaria indicar el serviceID de ServicesManager
        self.servicesList =  self.readFileConf('./serviceManager/conf.txt')
        #self.samplingController = SamplingController()
        #self.locationSensor = LocationSensor()
        #self.irradiationSensor = IrradiationSensor()
        #self.temperatureInteriorSensor = TemperatureInteriorSensor()
        #self.humiditySensor = HumiditySensor()
        #self.temperatureExteriorSensor = TemperatureExteriorSensor()


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

    def getAtributeConf(self, serviceID, atribute):
        fileName = self.servicesList[serviceID].get('path')
        atributos = self.readFileConf(fileName)
        value = atributos[atribute]
        return value

    def updateAtributeConf(self, serviceID, atribute, value): #Faltaria decir al service que actualice su parametro
        error = False
        fileName = self.servicesList[serviceID].get('path')  #Implementar diccionario con clave = serviceID y valor = fileNameConf
        atributes = self.readFileConf(fileName)
        atributes[atribute] = value
        self.writeFileConf(fileName, atributes)
        return error

    def wakeAllServices(self):  # TERMINAR
        if self.servicesList[2].get('serviceEnabled') == 1:
            self.temperatureExteriorSensor.start()


    '''  Funciones pendientes
    def start(self)

    def updateFileNameService(self, serviceID, fileName)  #¿Para que se usa?

    def startService(self, serviceID)

    def stopService(self, serviceID)

    def restartService(self, serviceID)
    '''


def main():
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


#main()
