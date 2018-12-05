import time
import gc
from machine import RTC


class SamplingController(object):

    def __init__(self):
        self.serviceID = 1
        self.enabled = False
        self.sensorsList = dict()
        self.sendingFrequency = 0
        self.sleepTime = 0
        self.wakeTime = 0
        self.rtc = 0
        self.conexion = 0

    #Tratar posibles errores
    def confService(self, atributes):
        self.conexion = atributes['connectionService']
        self.sendingFrequency = atributes['sendingFrequency']
        self.sleepTime = atributes['sleepTime']
        self.wakeTime = atributes['wakeTime']
        self.sensorsList = atributes['sensorsList']

    def start(self):
        if 2 in self.sensorsList:
            coordinates = self.sensorsList.setdefault(2).getLocation()
            self.rtc = RTC()
            print(self.rtc.now())
            print("Longitude: " + str(coordinates[0]))
            print("Latitude: " + str(coordinates[1]))
            print("Height: " + str(coordinates[2]))
            # Enviar mensaje con la posicion y la hora
        else:
            error = -1 # GPS no esta activado
            self.rtc = RTC() # ¿Como inicializar RTC?
        self.sendData()

    def setServicesList(self, sensorsList):
        self.sensorsList = sensorsList

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'servicesList':
            self.servicesList = newValue
        elif atribute == 'sendingFrequency':
            self.sendingFrequency = newValue
        elif atribute == 'sleepTime':
            self.sleepTime = newValue
        elif atribute == 'wakeTime':
            self.wakeTime = newValue
        else:
            error = True # error de atributo incorrecto -8
        return error

    def sendData(self): # Modificar para enviar datos a mensajeriaSensor
        self.ram()
     	i = 0
    	dataSend = 0# dict()
        while True:
            data = dict()
            time.sleep(self.sendingFrequency)
            print("-----------------------------------------------------------Iteracion numero = " + str(i) + "---------------------------------------------------------------")
            for sensor, valor in self.sensorsList.items():
            	muestra = valor.getData()
            	data.setdefault(sensor, muestra)
            	dataSend = str(sensor) + " : " + str(muestra)
                print(dataSend)
            	self.ram()
            self.conexion.sendPackage(1, data)
            del data
            self.ram()
            i += 1


    def connect(self, atributes):
        self.enabled = False
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False


    ''' Funciones pendientes
    def sleep(self):

    def wakeUp(self):
    '''
