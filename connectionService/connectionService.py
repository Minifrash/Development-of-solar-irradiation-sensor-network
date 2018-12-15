import time
from machine import RTC
from network import LoRa
import socket
import ubinascii
from libraries.ram import *

class ConnectionService(object):

    def __init__(self):
        self.serviceID = 7
        self.conexion = 0
        self.rtc = 0
        self.euiGateway = 0
        self.keyGateway = 0

    def confService(self, atributes):
        self.rtc = RTC()
        self.euiGateway = atributes['euiGateway']
        self.keyGateway = atributes['keyGateway']
    	lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868) # Initialise LoRa in LORAWAN mode. Europe = LoRa.EU868
    	# create an OTAA authentication parameters
    	app_eui = ubinascii.unhexlify(self.euiGateway) # eui del Gateway
    	app_key = ubinascii.unhexlify(self.keyGateway) # key del gateway
    	lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0) # join a network using OTAA (Over the Air Activation)
    	while not lora.has_joined(): # wait until the module has joined the network
    	    time.sleep(2.5)
    	    print('Not yet joined...')

    	self.conexion = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket
    	self.conexion.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # set the LoRaWAN data rate

    def connect(self, atributes):
        self.confService(atributes)
        self.sendPackage('connect', '')

    def disconnect(self):
        self.sendPackage('disconnect', '')

    def sendPackage(self, typePackage, data):
        dataSend = ''
        if typePackage == 'sample': # Mensaje de muestras
            dataSend = self.samplePackage(data)
        if typePackage == 'sincroGPS': # Mensaje de muestras
            dataSend = self.sincroGPSPackage(data)
        if typePackage == 'noSincroGPS': # Mensaje de muestras
            dataSend = self.noSincroGPSPackage()
        if typePackage == 'sleep': # Mensaje de muestras
            dataSend = self.sleep(data)
        if typePackage == 'connect': # Mensaje para darse de anta en thingsboards
            dataSend = self.connectPackage(data)
        if typePackage == 'disconnect': # Mensaje para darse de baja en thingsboards
            dataSend = self.disconnectPackage(data)
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
        collectRAM()

    def samplePackage(self, data):
    	dataSend = ''
    	dataSend += str(data.get('hour')) # Hora dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(data.get('minute')) # Minuto dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(data.get('seconds')) # Segundo dataSend += str(self.rtc.now()[5]) # Segundo
        dataSend += ' '
        dataSend += '0' # Type of package 0 = sample
        dataSend += ' '

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

        dataSend += ' '
        dataSend += str(data.get('Batt'))
        return dataSend

    def sincroGPSPackage(self, data):
        dataSend = ''
    	dataSend += str(data.get('hour')) # Hora dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(data.get('minute')) # Minuto dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(data.get('seconds')) # Segundo dataSend += str(self.rtc.now()[5]) # Segundo
        dataSend += ' '
        dataSend += '1' # Type of package 1 = sincroGPS
        dataSend += ' '
        dataSend += str(data['longitude'])
        dataSend += ' '
        dataSend += str(data['latitude'])
        dataSend += ' '
        dataSend += str(data['height'])
        return dataSend

    def noSincroGPSPackage(self, data): # ¿Siempre pasar hora de inicio 00:00:00?
        dataSend = ''
    	dataSend += str(data.get('hour')) # Hora dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(data.get('minute')) # Minuto dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(data.get('seconds')) # Segundo dataSend += str(self.rtc.now()[5]) # Segundo
        dataSend += ' '
        dataSend += '2' # Type of package 2 = noSincroGPS
        dataSend += ' '
    	dataSend += '00' # Hora Inicio
    	dataSend += ' '
    	dataSend += '00' # Minuto Inicio
    	dataSend += ' '
    	dataSend += '00' # Segundo Inicio
        return dataSend

    def sleep(self, data):
        dataSend = ''
    	dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[5]) # Segundo
        dataSend += ' '
        dataSend += '5' # Type of package 3 = sleep
        dataSend += ' '
        dataSend += str(data)
        return dataSend

    def connectPackage(self, data):
        dataSend = ''
    	dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[5]) # Segundo
        dataSend += ' '
        dataSend += '3' # Type of package 3 = connect
        return dataSend

    def disconnectPackage(self, data):
        dataSend = ''
    	dataSend += str(self.rtc.now()[3]) # Hora
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[4]) # Minuto
    	dataSend += ' '
    	dataSend += str(self.rtc.now()[5]) # Segundo
        dataSend += ' '
        dataSend += '4' # Type of package 4 = disconnect
        return dataSend
