from twisted.internet import protocol
from twisted.web import resource
from twisted.protocols import basic


class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        self.transport.write(self.factory.getUser(user)+"\r\n")
        self.transport.loseConnection()


class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol

    def __init__(self):
        self.users = {
            'Jimmy': 'You want a piece of me, boy?',
            'Bobby': 'Gotta WHOLE lotta love!'
        }

    def getUser(self, user):
        return self.users.get(user, "No such user")


class SomeLeafResource(resource.Resource):

    isLeaf = True

    def render(self, request):
        return 'Message handled!'

