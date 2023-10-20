import json, time, random
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import sharedData
from PdClient import *


def generateNewMode():
    newMode = sharedData.mode
    while newMode == sharedData.mode:
        newMode = random.randint(0, len(sharedData.modes) - 1)
        if len(sharedData.modes) == 1:
            break
    sharedData.numInstancesForMode = random.choice(
        range(
            sharedData.modes[newMode]["minInstances"],
            sharedData.modes[newMode]["maxInstances"] + 1,
        )
    )
    print("new mode: ", sharedData.modes[newMode]["mode"])
    return newMode


def runEverySecond():
    """
    Called at every loop interval.
    """
    global startTime

    if startTime + sharedData.numSecsToNextMode <= time.time():
        sharedData.mode = generateNewMode()
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
    f = open(
        "test3.json",
    )
    data = json.load(f)
    sharedData.modes = data["modes"]
    startTime = time.time() - sharedData.numSecsToNextMode

    for i in range(sharedData.numPdInstances):
        port = 3000 + sharedData.activeTrees[i]
        reactor.connectTCP("localhost", port, PdClientFactory(i))
    loop = task.LoopingCall(runEverySecond)
    loopDeferred = loop.start(1.0)
    loopDeferred.addErrback(ebLoopFailed)

    reactor.run()
