import time
import gc
from machine import RTC
from network import LoRa
import socket
import ubinascii


class ConnectionService(object):

    def __init__(self):
        self.conexion = 0
        self.rtc = 0
	    self.euiGateway = 0
	    self.keyGateway = 0

    def confService(self, atributes):
        self.rtc = RTC()
	    self.euiGateway = atributes['euiGateway']
	    self.keyGateway = atributes['keyGateway']
        # Initialise LoRa in LORAWAN mode. Europe = LoRa.EU868
    	lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    	# create an OTAA authentication parameters
    	app_eui = ubinascii.unhexlify(self.euiGateway) # eui del Gateway
    	app_key = ubinascii.unhexlify(self.keyGateway) # key del gateway
    	# join a network using OTAA (Over the Air Activation)
    	lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    	# wait until the module has joined the network
    	while not lora.has_joined():
    	    time.sleep(2.5)
    	    print('Not yet joined...')

    	# create a LoRa socket
    	self.conexion = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    	# set the LoRaWAN data rate
    	self.conexion.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    def connect(self, atributes):
        self.confService(atributes)

    #def disconnect(self):
        #Desconectar conexion LoRa

    def sendPackage(self, typePackage, data):
        if typePackage == 'sample': # Mensaje de muestras
            dataSend = self.samplePackage(data)
        if typePackage == 'sincroGPS': # Mensaje de muestras
            dataSend = self.sincroGPSPackage(data)
        if typePackage == 'noSincroGPS': # Mensaje de muestras
            dataSend = self.noSincroGPSPackage(data)
        self.send(dataSend)

    def send(self, dataSend):
    	# make the socket blocking
    	self.conexion.setblocking(True)
    	# send some data
    	self.conexion.send(dataSend)
    	# make the socket non-blocking
    	self.conexion.setblocking(False)
    	# get any data received (if any...)
    	dataRecv = self.conexion.recv(64)
        gc.collect()


    def samplePackage(self, data):
    	dataSend = ''
    	dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[5]) # Segundo
	    dataSend += ' '
        dataSend += '0' # Type of package 0 = sample

        if 3 in data:
            dataSend += str(1)
            dataSend += ' '
        else:
            dataSend += str(0)
            dataSend += ' '

        if 4 in data:
            dataSend += str(1)
            dataSend += ' '
        else:
            dataSend += str(0)
            dataSend += ' '

        if 5 in data:
            dataSend += str(1)
            dataSend += ' '
        else:
            dataSend += str(0)
            dataSend += ' '

        if 6 in data:
            dataSend += str(1)
            dataSend += ' '
        else:
            dataSend += str(0)
            dataSend += ' '

    	if 3 in data:
            dataSend += str(data.get(3))
            dataSend += ' '
        if 4 in data:
            dataSend += str(data.get(4))
            dataSend += ' '
        if 5 in data:
            dataSend += str(data.get(5))
            dataSend += ' '
        if 6 in data:
            dataSend += str(data.get(6))
        #self.send(dataSend)


    def sincroGPSPackage(self, data):
        dataSend = ''
    	dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[5]) # Segundo
	    dataSend += ' '
        dataSend += '1' # Type of package 1 = sincroGPS
        dataSend += str(data.get(0))
        dataSend += ' '
        dataSend += str(data.get(1))
        dataSend += ' '
        dataSend += str(data.get(2))
        #self.send(dataSend)


    def noSincroGPSPackage(self, data):
        dataSend = ''
    	dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[5]) # Segundo
	    dataSend += ' '
        dataSend += '2' # Type of package 1 = noSincroGPS
        #self.send(dataSend)
