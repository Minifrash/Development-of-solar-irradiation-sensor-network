from machine import RTC

class ErrorLogService(object):

    def __init__(self):
        self.serviceID = 8
        self.rtc = 0
        self.enabled = False
        self.namesFiles = dict()
        self.warningLog = dict()
        self.connectionService = 0
        self.descriptionsErrors = dict()
        self.descriptionsWarnings = dict()

    def confService(self, atributes):
        self.namesFiles.setdefault('errorFile', atributes['errorFile'])
        self.namesFiles.setdefault('warningFile', atributes['warningFile'])
        self.rtc = RTC()
        self.connectionService = atributes['connectionService']
        self.descriptionsErrors = atributes['errorsList']
        self.descriptionsWarnings = atributes['warningsLits']

    def updateAtribute(self, atribute, newValue): # Probar
	if atribute == 'errorFile':
		self.namesFiles.update({atribute: newValue})
	elif atribute == 'warningFile':
		self.namesFiles.update({atribute: newValue})
	elif atribute == 'descriptionsErrors':
		self.descriptionsErrors = newValue
	elif atribute == 'descriptionsWarnings':
		self.descriptionsWarnings = newValue
	else:
		self.regError(self.serviceID, -8) #Incorrect Atribute Error code

    def connect(self, atributes):
        self.confService(atributes)
        self.enabled = True

    def regError(self, serviceID, error):
	if self.enabled == True:
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
		self.notifyError(error)
	    if error in self.descriptionsWarnings:
		description = self.descriptionsWarnings[error].get('description') #self.descriptionsWarnings.setdefault(error) 
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
	if(counter < self.descriptionsWarnings[error].get('erLimit')): #self.erCounter): 
	    counter += 1
	    self.warningLog[serviceID].update({error: counter})
	else:
	    self.notifyWarning(error)
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

    def notifyError(self, error):
        dataSend = dict()
        dataSend.setdefault('hour', self.rtc.now()[3])
        dataSend.setdefault('minute', self.rtc.now()[4])
        dataSend.setdefault('seconds', self.rtc.now()[5])
        dataSend.setdefault('description', self.descriptionsErrors.setdefault(error))
        self.connectionService.sendPackage('errorWarning', dataSend)

    def notifyWarning(self, warning):
        dataSend = dict()
        dataSend.setdefault('hour', self.rtc.now()[3])
        dataSend.setdefault('minute', self.rtc.now()[4])
        dataSend.setdefault('seconds', self.rtc.now()[5])
        dataSend.setdefault('description', self.descriptionsWarnings[warning].get('description'))#self.descriptionsWarnings.setdefault(warning)
        self.connectionService.sendPackage('errorWarning', dataSend)

    def disconnect(self):
	self.enabled = False

    def serviceEnabled(self):
        return self.enabled
