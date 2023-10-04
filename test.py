import json, time, random
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

from PdClient import *


numPdInstances = 2
PdActive = [0] * numPdInstances
numSecsToNextMode = 60
mode = 0

def generateNewMode(mode):
    global modes
    
    newMode = mode
    while (newMode == mode):
        newMode = random.randint(0,len(modes)-1)
    return newMode

f = open('test.json',)
data = json.load(f)
modes = data['modes']
startTime = time.time() - 60

def runEverySecond():
    """
    Called at every loop interval.
    """
    global startTime, mode
    
    if startTime + numSecsToNextMode <= time.time():
            mode = generateNewMode(mode)
            print("new mode ", mode)
            startTime = time.time()
    return

    # We looped enough times.
    loop.stop()
    return

def ebLoopFailed(failure):
    """
    Called when loop execution failed.
    """
    print(failure.getBriefTraceback())
    reactor.stop()
    
if __name__ == "__main__":
    
    for i in range(numPdInstances):
        reactor.connectTCP("localhost", 3001 + i, PdClientFactory(3001 + i))

    print("starting looping call")
    loop = task.LoopingCall(runEverySecond)
    loopDeferred = loop.start(1.0)
    loopDeferred.addErrback(ebLoopFailed)

    reactor.run()
    
    print("I don't think I'll see this")   
    # while True:
  