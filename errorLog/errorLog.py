from machine import RTC

class ErrorLog(object):

    def __init__(self):
        self.serviceID = 8
        self.rtc = 0
        self.namesFiles = dict()
        self.warningLog = dict()
        self.sensorsList = dict()
        self.noSensorsList = dict()
        self.descriptionsErrors = dict()
        self.descriptionsWarnings = dict()
        self.erCounter = 5

    def confService(self, atributes):
        self.namesFiles.setdefault('errorFile', atributes['errorFile'])
        self.namesFiles.setdefault('warningFile', atributes['warningFile'])
        self.rtc = RTC()
        self.sensorsList = atributes['sensorsList']
        self.noSensorsList = atributes['noSensorsList']
        self.descriptionsErrors = atributes['descriptionsErrors']
        self.descriptionsWarnings = atributes['descriptionsWarnings']

    def setSensorsList(self, sensorsList):
        self.sensorsList = sensorsList

    def setnoSensorsList(self, noSensorsList):
        self.noSensorsList = noSensorsList

    def connect(self, atributes):
        self.confService(atributes)

    def regError(self, serviceID, error):
        fileError = open(self.namesFiles['errorFile'], "a")
        fileWarning = open(self.namesFiles['warningFile'], "a")
        fileError.close()
        fileWarning.close()
        description = ""
        time = ""
        time += str(self.rtc.now()[3]) # Hora
    	time += ':'
    	time += str(self.rtc.now()[4]) # Minuto
    	time += ':'
    	time += str(self.rtc.now()[5]) # Segundo
        if error in self.descriptionsErrors:
            description = self.descriptionsErrors.setdefault(error)
            self.updateFile(self.namesFiles.get('errorFile'))
            fileError = open(self.namesFiles.get('errorFile'), "a")
            fileError.write(time + " " + str(serviceID) + " " + description + "/n")
            fileError.close()
            self.notifyError()
        if error in self.descriptionsWarnings:
            description = self.descriptionsWarnings.setdefault(error)
            counter = self.counterCheck(serviceID, error) #Comprobación de contador
            self.updateFile(self.namesFiles.get('warningFile'))
            fileWarning = open(self.namesFiles.get('warningFile'), "a")
            fileWarning.write(time + " " + str(serviceID) + " " + description + " " + str(counter) + "\n")
            fileWarning.close()

    def counterCheck(self, serviceID, error):
	if serviceID not in self.warningLog:
	    aux = dict()
	    self.warningLog.setdefault(serviceID, aux)
	if error not in self.warningLog[serviceID]:
	    self.warningLog[serviceID].setdefault(error, 0)
        counter = self.warningLog[serviceID].setdefault(error) #Comprueba cuantas veces ha sucedido "error"
        if(counter < self.erCounter):
            counter += 1
	    self.warningLog[serviceID].update({error: counter})
        else:
	    print("Se procede a reiniciar el servicio con ID: " + str(serviceID))
            #self.sensorsList.setdefault(serviceID).disconnect()
            #self.sensorsList.setdefault(serviceID).connect()
            counter = 0
	    self.warningLog[serviceID].update({error: counter})
        return counter

    def updateFile(self, fileName):
        f = open(fileName, "r")
	lines = f.readlines()
	f.close()
	if len(lines) == 10: #Si la longitud del fichero era 10, se crea de nuevo vacio copiando solo las lineas 1-9
	    fileaux = open(fileName, "w")
	    i = 1
	    while i < 10:
	    	fileaux.write(lines[i])
		i += 1
	    fileaux.close()

    def notifyError(self):
        self.noSensorsServicesList.setdefault(7).sendPackage('error', dataSend)

