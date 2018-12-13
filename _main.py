from serviceManager.serviceManager import ServiceManager
from libraries.ram import *
import _thread
import time
from machine import deepsleep


collectRAM()
showMemoryRAM()

sm = ServiceManager()
#sm.confService()
#sm.startService(1)
#sm.startService(3)
#sm.startService(4)
#sm.startService(5)
#sm.startService(6)
sm.start()
#sm.stopService(3)
#sm.stopService(4)
#sm.stopService(5)
#sm.stopService(6)
#sm.stopService(1)
#sm.getruta()

#_thread.start_new_thread(sm.start, ())


#time.sleep(30)

#print('A dormir 2 min')
#deepsleep(120000)
#print('A despertar de la siesta de 2 min')

#time.sleep(10)
#sm.stopService(3)
#sm.stopService(4)
#time.sleep(5)
#sm.startService(3)
#time.sleep(15)
#sm.startService(4)
#sm.updateAtributeConf(5, 'mode', 0)
#sm.updateAtributeConf(6, 'samplingFrequency', 1)

#print(sm.getAtributeConf(5, 'mode'))
#print(sm.getAtributeConf(6, 'samplingFrequency'))

#_thread.exit()
