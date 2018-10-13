from samplingController.samplingController import SamplingController
from temperatureExteriorSensor.temperatureExteriorSensor import TemperatureExteriorSensor

class ServiceManager(object):

    def __init__(self):
        self.serviceID = 0 # Faltaria indicar el serviceID de ServicesManager
        self.servicesList =  self.readFileConf("confFile.txt")
        self.samplingController = SamplingController()
        #self.locationSensor = LocationSensor()
        #self.irradiationSensor = IrradiationSensor()
        #self.temperatureInteriorSensor = TemperatureInteriorSensor()
        #self.humiditySensor = HumiditySensor()
        self.temperatureExteriorSensor = TemperatureExteriorSensor()


    def addServicesList(self, serviceID, path, serviceEnabled):
        newService = {'path': path, 'serviceEnabled':serviceEnabled}
        error = self.servicesList.setdefault(serviceID, newService)
        self.writeFileConf (self.servicesList[self.serviceID][path], self.servicesList):
        return error

    def deleteServiceList(self, serviceID):
        deleteService = selt.servicesList.pop('serviceID')
        # Tratar posible error que devuelba pop()

    def getservicesList(self):
        return self.servicesList

    def readFileConf (self, fileName):
        '''  Codigo si hubise fallos con dic = eval(f.read())
        dic = dict()
        for linea in open(fileName, "r"):
            linea.strip()
            clave,  valor = linea.split()
            dic.setdefault(clave, valor)
        '''
        f = open(fileName, "r")
        dic = eval(f.read())
        f.close()
        return dic

    # REPASAR ¿Como se refleja un posible error?
    def writeFileConf (fileName, data):
        error = False
        f = open(fileName, "w")
        f.write(str(data))

        '''   Codigo si hubise fallos con f.write(str(data))
        lista = data.keys()
        for clave in lista:
            value = data[clave]
            line = clave + ' ' + str(value) + '\n' # usar str porque no deja concatenar string con int
            f.write(line)
        '''
        f.close()
        return error

    def getAtributeConf(self, serviceID, atribute):
        fileName = self.servicesList[serviceID][path]  #Implementar diccionario con clave = serviceID y valor = fileNameConf
        #fileName = 'entrada.txt'
        atributos = self.readFileConf(fileName)
        value = atributos[atribute]
        return value

    def updateAtributeConf(self, serviceID, atribute, value):
        error = False
        fileName = self.servicesList[serviceID][path]  #Implementar diccionario con clave = serviceID y valor = fileNameConf
        #fileName = 'entrada.txt'
        atributes = self.readFileConf(fileName)
        atributes[atribute] = value
        writeFileConf(fileName, atributes)
        return error

    def wakeAllServices():
        if self.servicesList[2]['serviceEnabled'] == 1:
            self.temperatureExteriorSensor.start()

def main():
    services = ServicesManager()
    #services.addServicesList()
    #dic = services.getservicesList()
    dic = services.readFileConf("entrada.txt")
    print(dic.items())

    return 0

main()
