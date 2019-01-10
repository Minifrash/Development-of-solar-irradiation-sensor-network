import _thread
import time

class TemperatureInSensor(object):

    def __init__(self):
        self.serviceID = 4
        self.enabled = False
        self.samplingFrequency = 0
        self.mode = 0
        self.dht22Sensor = 0
        self.lock = 0
        self.errorLogService = 0

    def confService(self, atributes):
        self.lock = atributes['lock']
        self.dht22Sensor = atributes['dht22Sensor']
	self.errorLogService = atributes['errorLogService']
	if ('mode' in atributes) and ('samplingFrequency' in atributes):
	    if not str(atributes['samplingFrequency']).isdigit() or atributes['samplingFrequency'] < 0: #Comprobar si es un numero (isdigit) y si es negativo
        	self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
		self.samplingFrequency = atributes['samplingFrequency']
            if not str(atributes['mode']).isdigit() or atributes['mode'] < 0: #Comprobar si es un numero (isdigit) y si es negativo
		self.errorLogService.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
		self.mode = atributes['mode']
	else:
	    self.errorLogService.regError(self.serviceID, -2) #ConfFile Error

    def start(self):
        atributes = dict()
        atributes.setdefault('serviceID', self.serviceID)
        atributes.setdefault('lock', self.lock)
        atributes.setdefault('samplingFrequency', self.samplingFrequency)
        atributes.setdefault('errorLogService', self.errorLogService)
        self.dht22Sensor.connect(atributes)

    def updateAtribute(self, atribute, newValue):
        if not str(newValue).isdigit() or newValue < 0: #¿Lo hace serviceManager?
            self.errorLogService.regError(self.serviceID, -9 ) #Incorrect AtributeValue Error
        if atribute == 'samplingFrequency':
            self.samplingFrequency = newValue
            self.dht22Sensor.updateAtribute('samplingFrequency', self.samplingFrequency)
        elif atribute == 'mode':
            self.mode = newValue
        else:
            self.errorLogService.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def getData(self):
        data = self.dht22Sensor.getTemperature(self.mode)
        return data

    def connect(self, atributes):
        self.enabled = True
        self.confService(atributes)
        self.start()

    def disconnect(self):
        self.enabled = False
        self.dht22Sensor.disconnect(self.serviceID)

    def serviceEnabled(self):
        return self.enabled
