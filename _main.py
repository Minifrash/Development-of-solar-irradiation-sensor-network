from serviceManager.serviceManager import ServiceManager
from libraries.ram import *
import _thread
import time


collectRAM()
showMemoryRAM()

sm = ServiceManager()
sm.start()

# Test
#_thread.start_new_thread(sm.start, ())
#time.sleep(30)
#sm.stopService(3)
#sm.stopService(4)
#sm.stopService(5)

# Test irradiationSensor
#time.sleep(30)
#print("Test irradiationSensor")
#sm.startService(3)
#print("Configuracion Inicial")
#print('mode: ' + str(sm.getAtributeConf(3, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(3, 'samplingFrequency')))
#sm.updateAtributeConf(3, 'mode', 1)
#sm.updateAtributeConf(3, 'samplingFrequency', 2)
#print("Configuracion actualizada")
#print('mode: ' + str(sm.getAtributeConf(3, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(3, 'samplingFrequency'))

# Test tempertureInSensor
#time.sleep(30)
#print("Test tempertureInSensor")
#sm.startService(4)
#print("Configuracion Inicial")
#print('mode: ' + str(sm.getAtributeConf(4, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(4, 'samplingFrequency'))
#sm.updateAtributeConf(4, 'mode', 1)
#sm.updateAtributeConf(4, 'samplingFrequency', 2)
#print("Configuracion actualizada")
#print('mode: ' + str(sm.getAtributeConf(4, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(4, 'samplingFrequency'))

# Test humiditySensor
#time.sleep(30)
#print("Test humiditySensor")
#sm.startService(5)
#print("Configuracion Inicial")
#print('mode: ' + str(sm.getAtributeConf(5, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(5, 'samplingFrequency'))
#sm.updateAtributeConf(5, 'mode', 1)
#sm.updateAtributeConf(5, 'samplingFrequency', 2)
#print("Configuracion actualizada")
#print('mode: ' + str(sm.getAtributeConf(5, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(5, 'samplingFrequency'))

# Test temperatureOutSensor
#time.sleep(30)
#print("Test temperatureOutSensor")
#sm.startService(6)
#print("Configuracion Inicial")
#print('mode: ' + str(sm.getAtributeConf(6, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(6, 'samplingFrequency'))
#sm.updateAtributeConf(6, 'mode', 1)
#sm.updateAtributeConf(6, 'samplingFrequency', 2)
#print("Configuracion actualizada")
#print('mode: ' + str(sm.getAtributeConf(6, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(6, 'samplingFrequency'))

# Test locationSensor
#time.sleep(30)
#print("Test locationSensor")
#sm.startService(2)
#print("Configuracion Inicial")
#print('mode: ' + str(sm.getAtributeConf(2, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(2, 'samplingFrequency'))
#sm.updateAtributeConf(2, 'mode', 1)
#sm.updateAtributeConf(2, 'samplingFrequency', 2)
#print("Configuracion actualizada")
#print('mode: ' + str(sm.getAtributeConf(2, 'mode')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(2, 'samplingFrequency'))
#sm.updateAtributeConf(2, 'mode', 0)

# Test samplingController
#time.sleep(30)
#print("Test samplingController")
#sm.startService(1)
#print("Configuracion Inicial")
#print('sleepTime: ' + str(sm.getAtributeConf(1, 'sleepTime')))
#print('wakeTime: ' + str(sm.getAtributeConf(1, 'wakeTime')))
#print('sendingFrequency: ' + str(sm.getAtributeConf(1, 'sendingFrequency'))
#sm.updateAtributeConf(1, 'sleepTime', '18:00:00')
#sm.updateAtributeConf(1, 'wakeTime', '10:00:00')
#sm.updateAtributeConf(1, 'sendingFrequency', 10)
#print("Configuracion actualizada")
#print('sleepTime: ' + str(sm.getAtributeConf(1, 'sleepTime')))
#print('wakeTime: ' + str(sm.getAtributeConf(1, 'wakeTime')))
#print('sendingFrequency: ' + str(sm.getAtributeConf(1, 'sendingFrequency'))
#sm.updateAtributeConf(1, 'sleepTime', '17:00:00')
#sm.updateAtributeConf(1, 'wakeTime', '09:00:00')

# Test connectionService
#time.sleep(30)
#print("Test connectionService")
#sm.startService(7)
#print("Configuracion Inicial")
#print('euiGateway: ' + str(sm.getAtributeConf(7, 'euiGateway')))
#print('keyGateway: ' + str(sm.getAtributeConf(7, 'keyGateway'))
#sm.updateAtributeConf(2, 'euiGateway', 'ada4dae3ac12676a')
#sm.updateAtributeConf(2, 'keyGateway', '11b0282a189b75b0b4d2d8c7fa38548a')
#print("Configuracion actualizada")
#print('mode: ' + str(sm.getAtributeConf(2, 'euiGateway')))
#print('samplingFrequency: ' + str(sm.getAtributeConf(2, 'keyGateway'))
#sm.updateAtributeConf(2, 'euiGateway', 'ada4dae3ac12676b')
#sm.updateAtributeConf(2, 'keyGateway', '11b0282a189b75b0b4d2d8c7fa38548b')

#_thread.exit()
