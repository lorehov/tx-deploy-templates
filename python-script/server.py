import os
import syslog
import sys
import ConfigParser

from twisted.internet import protocol, reactor
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.protocols import basic
from twisted.python import usage, log
from twisted.python.logfile import DailyLogFile

from twisted.web import server, resource


class Options(usage.Options):

    optParameters = [
        ["logfile", "l", "twisted.log", "Where to put logs"],
        ["reactor", "r", "select", "Nuclear plant type"],
        ["config", "c", "config.json", "Where are the settings lies"]
    ]

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

    #setting up logging
    logDest = opts['logfile']
    try:
        if logDest == 'syslog':
            syslog.startLogging('z4r')
        elif logDest == 'stdout':
            log.startLogging(sys.stdout)
        else:
            log.startLogging(DailyLogFile(os.path.basename(logDest), os.path.dirname(logDest)))
    except Exception, ex:
        log.startLogging(sys.stdout)
        log.msg(str(ex))

    #setting up reactor
    if opts['reactor'] == 'epoll':
        from twisted.internet import epollreactor
        epollreactor.install()

    #reading config
    config = ConfigParser.ConfigParser()
    config.read(opts['config'])

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