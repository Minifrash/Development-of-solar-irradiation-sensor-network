import _thread
import time

class TemperatureInSensor(object):

    def __init__(self):
        self.serviceID = 4
        self.enabled = False
        self.samplingFrequency = 0
        self.mode = 0
        self.lastTemperature = 0
        self.sumTemperature = 0
        self.sampleCounter = 0
        self.sampleThread = 0
        self.temp = 0
        self.dht = 0
        self.lock = 0
        self.errorLog = 0

    def confService(self, atributes):
        self.lock = atributes['lock']
        self.dht = atributes['dht']
        self.samplingFrequency = atributes['samplingFrequency']
	self.errorLog = atributes['errorLog']
        self.mode = atributes['mode']
        if not str(self.samplingFrequency).isdigit() or self.samplingFrequency < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error
        if not str(self.mode).isdigit() or self.mode < 0: #Comprobar si es un numero (isdigit) y si es negativo
            self.errorLog.regError(self.serviceID, -9) #Incorrect AtributeValue Error

    def start(self):
        atributes = dict()
	atributes.setdefault('serviceID', self.serviceID)
	atributes.setdefault('lock', self.lock)
	atributes.setdefault('samplingFrequency', self.samplingFrequency)
	atributes.setdefault('errorLog', self.errorLog)
        self.dht.connect(atributes)

    def updateAtribute(self, atribute, newValue):
        if not str(newValue).isdigit() or newValue < 0: #¿Lo hace serviceManager?
            self.errorLog.regError(self.serviceID, -9 ) #Incorrect AtributeValue Error
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
        elif atribute == 'mode':
            self.mode = newValue
        else:
            self.errorLog.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def getData(self):
        data = self.dht.getTemperature(self.mode)
        return data

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False
        self.dht.disconnect(self.serviceID)

    def serviceEnabled(self):
        return self.enabled
