from machine import RTC
import _thread
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
	self.errorsCounter = dict()
	self.warningsCounter = dict()
	self.lock = 0

    def confService(self, atributes):
	self.connectionService = atributes['connectionService']
	self.lock = atributes['lock']
        self.rtc = RTC()
	if ('errorFile' in atributes) and ('warningFile' in atributes) and ('errorsList' in atributes) and ('warningsLits' in atributes):
	    if str(atributes['errorFile']).isdigit(): #Error si es un numero
        	self.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
		self.namesFiles.setdefault('errorFile', atributes['errorFile'])
            if str(atributes['warningFile']).isdigit(): #Error si es un numero
        	self.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
		self.namesFiles.setdefault('warningFile', atributes['warningFile'])
	    if str(atributes['errorsList']).isdigit(): #Error si es un numero
        	self.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
		self.descriptionsErrors = atributes['errorsList']
	    if str(atributes['warningsLits']).isdigit(): #Error si es un numero
        	self.regError(self.serviceID, -9) #Incorrect AtributeValue Error
	    else:
		self.descriptionsWarnings = atributes['warningsLits']
	else:
	    self.regError(self.serviceID, -2) #ConfFile Error

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
	    #fileError = open(self.namesFiles['errorFile'], "a")
	    #fileWarning = open(self.namesFiles['warningFile'], "a")
	    #fileError.close()
	    #fileWarning.close()
	    time = ""
	    dataSend = dict()
	    dataSend.setdefault('hour', self.rtc.now()[3])
	    dataSend.setdefault('minute', self.rtc.now()[4])
	    dataSend.setdefault('seconds', self.rtc.now()[5])
	    time += str(dataSend['hour']) # Hora
	    time += ':'
	    time += str(dataSend['minute']) # Minuto
	    time += ':'
	    time += str(dataSend['seconds']) # Segundo
	    if error in self.descriptionsErrors:
		description = self.descriptionsErrors.setdefault(error)
		self.updateFile(self.namesFiles.get('errorFile'))
		fileError = open(self.namesFiles.get('errorFile'), "a")
		fileError.write(time + " " + str(serviceID) + " " + description + "/n")
		fileError.close()
		if error not in self.errorsCounter:
		    self.errorsCounter.setdefault(description, 0)
		counter = self.errorsCounter.setdefault(description)
		counter = counter + 1
		self.errorsCounter.setdefault(description, counter)
		dataSend.setdefault('description', description)
		dataSend.setdefault('counter', self.errorsCounter.setdefault(description))
		#self.notifyToServer(dataSend)
		self.connectionService.sendPackage('errorWarning', dataSend)
	    if error in self.descriptionsWarnings:
		description = self.descriptionsWarnings[error].get('description') #self.descriptionsWarnings.setdefault(error) 
		counter = self.counterCheck(serviceID, error, description, dataSend) #Comprobación de contador
		#self.updateFile(self.namesFiles.get('warningFile'))
		#self.lock.acquire()
		#fileWarning = open(self.namesFiles.get('warningFile'), "a")
		#prueba = time + " " + str(serviceID) + " " + description + " " + str(counter) + "\n"
		#fileWarning.write(prueba)
		#fileWarning.close()
		#self.lock.release()

    def counterCheck(self, serviceID, error, description, dataSend):
	if serviceID not in self.warningLog:
	    aux = dict()
	    self.warningLog.setdefault(serviceID, aux)
	if error not in self.warningLog[serviceID]:
	    self.warningLog[serviceID].setdefault(error, 1)
	counter = self.warningLog[serviceID].setdefault(error) #Comprueba cuantas veces ha sucedido "error"
	if(counter < self.descriptionsWarnings[error].get('erLimit')): #self.erCounter): 
	    counter += 1
	    self.warningLog[serviceID].update({error: counter})
	else:
	    if description not in self.warningsCounter:
	    	self.warningsCounter.setdefault(description, 0)
	    notifyCounter = self.warningsCounter.setdefault(description)
	    notifyCounter = notifyCounter + 1
	    self.warningsCounter.update({description: notifyCounter})
	    dataSend.setdefault('description', description)
	    dataSend.setdefault('counter', self.warningsCounter.setdefault(description))
	    #self.notifyToServer(dataSend)
	    self.connectionService.sendPackage('errorWarning', dataSend)
	    counter = 1
	    self.warningLog[serviceID].update({error: counter})
	return counter

    def updateFile(self, fileName):
	#self.lock.acquire()
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
	#self.lock.release()

    #def notifyToServer(self, dataSend):
        #self.connectionService.sendPackage('errorWarning', dataSend)

    def disconnect(self):
	self.enabled = False

    def serviceEnabled(self):
        return self.enabled
