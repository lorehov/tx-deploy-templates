from twisted.internet import protocol, reactor
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.protocols import basic

from twisted.web import server, resource
from mservice import common


class Options(common.Options):

    optFlags = [
        ["verbose", "v", "Run verbosely"],
        ["fast", "f", "Run fast!"],
        ["ssl", "s", "Use SSL"]
    ]

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


def runApplication():
    opts = Options()
    opts.parseOptions()

    common.initLogs(opts['logfile'])

    common.installReactor(opts['reactor'])

    config = common.loadConfig(opts['config'])

    #starting services with options from config
    if opts['ssl']:
        reactor.listenSSL(
            config.getint('finger', 'port'),
            FingerFactory(),
            DefaultOpenSSLContextFactory(
                config.get('ssl', 'cert'),
                config.get('ssl', 'private')
            )
        )
        reactor.listenSSL(
            config.getint('web', 'port'),
            server.Site(SomeLeafResource()),
            DefaultOpenSSLContextFactory(
                config.get('ssl', 'cert'),
                config.get('ssl', 'private')
            )
        )
    else:
        reactor.listenTCP(config.getint('finger', 'port'), FingerFactory())
        reactor.listenTCP(config.getint('web', 'port'), server.Site(SomeLeafResource()))
    reactor.run()

if __name__ == '__main__':
    runApplication()