import time
import gc

class SamplingController(object):

    def __init__(self):
        self.serviceID = 1
        self.sensorsList = dict()
        self.sendingFrequency = 0
        self.samplingFrequency = 0 # ¿Haria falta?
        self.sleepTime = 0
        self.wakeTime = 0
        self.sampleThread = 0

    #Tratar posibles errores
    def confService(self, atributos):
        self.sendingFrequency = atributos['sendingFrequency']
        self.samplingFrequency = atributos['samplingFrecuency'] # ¿Haria falta?
        self.sleepTime = atributos['sleepTime']
        self.wakeTime = atributos['wakeTime']

    def setServicesList(self, sensorsList):
        self.sensorsList = sensorsList

    def start(self, sensorsList):
        self.sensorsList = sensorsList
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

    def sendData(self): # Modificar para enviar datos a mensajeriaSensor
        self.ram()
        for i in range(5):
            time.sleep(5)
            print("-----------------------------------------------------------Iteracion numero = " + str(i) + "---------------------------------------------------------------")
            for sensor, valor in self.sensorsList.items():
                print(str(sensor) + " : " + str(valor.getData()))
                self.ram()
        for thread in self.sensorsList.values():
            thread.disconnect()
        self.ram()

    def ram(self):
        gc.collect()
        print('-----------------------------')
        print('Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
        print('-----------------------------')

    ''' Funciones pendientes
    def sleep(self):

    def wakeUp(self):

    def connect(self)

    def disconnect(self)

    '''
