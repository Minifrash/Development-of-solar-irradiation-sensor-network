import gc

def collectRAM():
    if gc.mem_free() <= 13000:
        gc.collect()

def showMemoryRAM():
    print('-----------------------------')
    print('Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
