import json, time, random, argparse

from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import sharedData
from PdClient import *


def generateNewMode():
    global modeToUse
    
    newMode = sharedData.mode
    while newMode == sharedData.mode:
        if modeToUse == "All":
            newMode = random.randint(0, len(sharedData.modes) - 1)
        else:
            gotMode = False
            for i in range(len(sharedData.modes)):
                if sharedData.modes[i]["mode"] == modeToUse:
                    newMode = i
                    gotMode = True
                    break
            if not gotMode:
                raise IndexError("no such mode: " + modeToUse)
            break
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
    parser = argparse.ArgumentParser(
        prog="control",
        description="Control audio/leds/Beagleboards for Whispering Woodlands project",
    )
    parser.add_argument("jsonfile")
    parser.add_argument("-m", "--mode", default="All")
    args = parser.parse_args()
    modeToUse = args.mode

    f = open(
        args.jsonfile,
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
