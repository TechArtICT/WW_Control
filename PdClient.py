import json, time, random
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from test import *

class PdClient(Protocol):

    def __init__(self, instanceNumber=None):
        self.instanceNumber = instanceNumber

    def dataReceived(self, data):
        
        global numPdInstances
        
        # need to parse data here. There could be more than one message
        # x = f'{self.quote}  {str(data[:-1])}'
        x = (data.strip(b"\n"))
        y = x.split(b";")
        for z in y:
            if z == b'':
                break
            print(z)
            if z == b"got anything?":
                print("yes")
        print("done")
        two = str(numPdInstances)+";\n"
        print(numPdInstances)
        self.transport.write(two.encode('ascii'))    
        
class PdClientFactory(ReconnectingClientFactory):
    def __init__(self, quote=None):
        self.quote = quote

    def startedConnecting(self, connector):
        print('Starting to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        return PdClient(self.quote)

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)