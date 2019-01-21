import gc

def collectMemory():
    if gc.mem_free() <= 13000:
        gc.collect()

def showMemory():
    print('-----------------------------')
    print('Free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
