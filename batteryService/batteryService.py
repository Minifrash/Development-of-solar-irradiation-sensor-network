import sys
from machine import Pin, ADC, DAC

class BatteryService(object):

    def __init__(self):
        self.powerPin = 0
        self.adc = 0
        self.Battery = 0
        self.vBiasDAC = 0

    def confService(self):
        self.powerPin = Pin('P8', mode=Pin.OUT)
        self.adc = ADC()
        self.adc.vref(1058)
        self.vBiasDAC = DAC('P22')
        self.vBiasDAC.write(0.135) # approximately 0.5 V
        self.Battery = self.adc.channel(pin='P14', attn = ADC.ATTN_11DB)

    def getData(self):
        return self.Battery.voltage()

    def connect(self):
        self.confService()
