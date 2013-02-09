from zope.interface import implements

from twisted.web import server
from twisted.application import service, internet
from twisted.plugin import IPlugin
from twisted.python import usage
from mservice.application import FingerFactory, SomeLeafResource


class Options(usage.Options):

    optParameters = [
        ["reactor", "r", "select", "Nuclear plant type"],
        ["config", "c", "config.json", "Where are the settings lies"]
    ]

    optFlags = [
        ["verbose", "v", "Run verbosely"],
        ["fast", "f", "Run fast!"],
        ["ssl", "s", "Use SSL"]
    ]


class ServiceMaker(object):
    implements(service.IServiceMaker, IPlugin)
    tapname = "myprojct"
    description = "Run this! It'll make your dog happy."
    options = Options

    def makeService(self, options):
        serviceCollection = service.MultiService()
        internet.TCPServer(9111, FingerFactory()).setServiceParent(serviceCollection)
        internet.TCPServer(3000, server.Site(SomeLeafResource())).serServiceParent(serviceCollection)
        return serviceCollection

service = ServiceMaker()
