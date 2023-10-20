import json, time, random
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import sharedData
from test import *


class PdClient(Protocol):
    global numInstancesForMode

    def __init__(self, instanceNumber=None):
        self.instanceNumber = instanceNumber
        self.timeToNextInstance = 0

    def chooseSoundForPdToPlay(self):
        soundDict = sharedData.modes[sharedData.mode]["sounds"]
        probGen = random.randint(0, 100) / 100
        probSum = 0

        for i in soundDict.keys():
            probOfSound = soundDict[i]["probability"]
            if probOfSound + probSum >= probGen:
                return soundDict[i]["file"]
            probSum += probOfSound

    def givePdSomethingToDo(self):
        global numInstancesForMode

        # Mark instance not active
        sharedData.PdActive[self.instanceNumber] = 0

        if (
            sharedData.numInstancesForMode > sum(sharedData.PdActive)
            and int(time.time() * 1000) >= self.timeToNextInstance
        ):
            print("get instance to play")
            sound = self.chooseSoundForPdToPlay()
            stringToSend = "play " + sound + ";\n"
            print("stringToSend: ", stringToSend)
            self.transport.write(stringToSend.encode("ascii"))
            sharedData.PdActive[self.instanceNumber] = 1
            self.timeToNextInstance = random.randint(
                sharedData.modes[sharedData.mode]["minMsToNextInstance"]
                + int(time.time() * 1000),
                sharedData.modes[sharedData.mode]["maxMsToNextInstance"]
                + int(time.time() * 1000),
            )

    def dataReceived(self, data):
        # need to parse data here. There could be more than one message
        # x = f'{self.quote}  {str(data[:-1])}'
        x = data.strip(b"\n")
        y = x.split(b";")
        for z in y:
            if z == b"":
                break
            print(z)
            if z == b"got anything?":
                self.givePdSomethingToDo()
                print("yes")
            else:
                self.transport.write("nope".encode("ascii"))

        print("done")


class PdClientFactory(ReconnectingClientFactory):
    maxDelay = 2  # Maximum delay between connection attempts (in seconds)
    factor = 1.5  # Factor by which the delay increases after each attempt

    def __init__(self, instanceNum=None):
        self.instanceNum = instanceNum

    def startedConnecting(self, connector):
        # print("Starting to connect.")
        pass

    def buildProtocol(self, addr):
        print("Connected.")
        print("Resetting reconnection delay")
        self.resetDelay()
        return PdClient(self.instanceNum)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection.  Reason:", reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        # print("Connection failed. Reason:", reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
