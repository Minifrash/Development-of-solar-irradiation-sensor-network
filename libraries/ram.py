import gc

#class MemoryRAM(object):

#    def __init__(self):
#        self.minFreeMemory = 10000

def collectRAM():
    if gc.mem_free() <=10000:
        gc.collect()

def showMemoryRAM():
    print('-----------------------------')
    print('Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
