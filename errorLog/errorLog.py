from machine import RTC
#import gc

class ErrorLog(object):

    def __init__(self):
        self.serviceID = 8
        self.rtc = 0
        #self.fileError = 0
        #self.fileWarning = 0
        self.namesFiles = dict()
        self.warningLog = dict()
        self.errorAux = dict()
        self.sensorsList = dict()
        self.serviceManager = 0
        self.erCounter = 5

    def confService(self): #, atributes
        self.namesFiles.setdefault('errorFile', './errors.txt') #= atributes['namesFiles']
	self.namesFiles.setdefault('warningFile', './warnings.txt')
        self.rtc = RTC()
        #self.sensorsList = atributes['sensorsList']
        #self.serviceManager = atributes['serviceManager']

    def setServicesList(self, sensorsList):
        self.sensorsList = sensorsList

    def connect(self): #, atributes
        self.confService() #atributes

    def regError(self, serviceID, error):
        fileError = open(self.namesFiles.get('errorFile'), "a")
        fileWarning = open(self.namesFiles.get('warningFile'), "a")
	description = ""
        time = ""
        time += str(self.rtc.now()[3]) # Hora
    	time += ':'
    	time += str(self.rtc.now()[4]) # Minuto
    	time += ':'
    	time += str(self.rtc.now()[5]) # Segundo
        if error == -1: #OSError
            description = "OSError"
            self.updateFile(self.namesFiles.get('errorFile'))
            fileError.write(time + " " + str(serviceID) + " " + description + "/n")
            #self.notifyError()
        if error == -3: #CreateThread Error
            description = "CreateThreadError"
            self.updateFile(self.namesFiles.get('errorFile'))
            fileError.write(time + " " + str(serviceID) + " " + description + "/n")
            #self.notifyError()
        if error == -5: #NoService Error
            description = "NoServiceError"
            counter = self.counterCheck(serviceID, error) #Comprobación de contador
            self.errorAux.setdefault(error, counter)
            self.warningLog.setdefault(serviceID, self.errorAux)
	    self.updateFile(self.namesFiles.get('warningFile'))
            fileWarning.write(time + " " + str(serviceID) + " " + description + " " + counter + "\n")
        if error == -6: #Active Service Error
            description = "ActiveServiceError"
            counter = self.counterCheck(serviceID, error) #Comprobación de contador
            self.errorAux.setdefault(error, counter)
            self.warningLog.setdefault(serviceID, self.errorAux)
	    self.updateFile(self.namesFiles.get('warningFile'))
            fileWarning.write(time + " " + str(serviceID) + " " + description + " " + counter + "\n")
        if error == -7: #Non-Active Service Error
            description = "Non-ActiveServiceError"
            counter = self.counterCheck(serviceID, error) #Comprobación de contador
            self.errorAux.setdefault(error, counter)
            self.warningLog.setdefault(serviceID, self.errorAux)
	    self.updateFile(self.namesFiles.get('warningFile'))
            fileWarning.write(time + " " + str(serviceID) + " " + description + " " + counter + "\n")
        if error == -8: #Incorrect Atribute Error
            description = "IncorrectAtributeError"
	    self.updateFile(self.namesFiles.get('errorFile'))
            fileError.write(time + " " + str(serviceID) + " " + description + "\n")
            #self.notifyError()
        if error == -9: #Incorrect AtributeValue Error
            description = "IncorrectAtributeValueError"
	    self.updateFile(self.namesFiles.get('errorFile'))
            fileError.write(time + " " + str(serviceID) + " " + description + "\n")
            #self.notifyError()
        if error == -10: #ZeroDivisionError
            description = "ZeroDivisionError"
            counter = self.counterCheck(serviceID, error) #Comprobación de contador
            self.errorAux.setdefault(error, counter)
            self.warningLog.setdefault(serviceID, self.errorAux)
	    self.updateFile(self.namesFiles.get('warningFile'))
            fileWarning.write(time + " " + str(serviceID) + " " + description + " " + counter + "\n")
        if error == -11: #Incorrect Value Error
            description = "IncorrectValueErrorOnSensor"
	    self.updateFile(self.namesFiles.get('errorFile'))
            fileError.write(time + " " + str(serviceID) + " " + description + "\n")
            #self.notifyError()
        fileError.close()
        fileWarning.close()
#		gc.collect()

    def counterCheck(self, serviceID, error):
	counter = self.warningLog[serviceID].get(error) #Comprueba cuantas veces ha sucedido "error"
	if(counter == None): #No existía este registro antes
	    counter = 0
	    if(counter < self.erCounter):
		self.sensorsList.setdefault(serviceID).disconnect()
		self.sensorsList.setdefault(serviceID).connect()
		#self.serviceManager.restartService(serviceID)
		counter += 1
	    else:
		counter = 0
	return counter

    def updateFile(self, fileName):
	file = open(fileName, "r+")
	lines = file.readlines()
	print("Tamaño de fichero: " + str(len(lines)))
	if len(lines) == 10:
	    for i in range(0, 9):
		lines[i] = lines[i+1]
	file.close()

    #def notifyError():
        #send notice error to server

