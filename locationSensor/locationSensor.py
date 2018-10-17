import sys
import _thread
import time

class LocationSensor(object):

    def __init__(self):
        self.serviceID = 2
        self.mode = 0
        self.latitude = 0
        self.altitude = 0
        self.longitude = 0
        self.enabled = 0 # ¿Haria falta?
        self.sampleThread = 0 #_thread.start_new_thread(self.sampling, (self.samplingFrequency, 1))#0 # ¿Como inicializar?

    def confService(self, atributos):
        self.mode = atributos['mode']

    def start(self):
        # Crear el thread para la funcion sendData()
        self.sampleThread = _thread.start_new_thread(self.sampling, (self.samplingFrequency,2))

    '''def sincro(self):'''

    def updateAtribute(self, atribute, newValue):
        error = False
        if atribute == 'mode':
            self.mode = newValue
        else:
            error = True # error de atributo incorrecto
        return error


'''    def getData(self):
        data = -1 # Posible error
        if self.mode == 0:
            data = #normal ¿Mandar array de lat-lon-alt?
        elif self.mode == 1:
            data = #rafaga ¿?
        else:
            data = -1
        return data
'''

    def disconnect(self):
        try
            self.sampleThread = _thread.exit()
        except SystemExit:
            error = -1 #-1 es un ejemplo, dependerá de política de errores

    ''' Funciones Pendientes

    def connect(self):

    def serviceEnabled(self):
        return enabled
    '''
