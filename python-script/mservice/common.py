import ConfigParser
import os
import syslog
import sys
from twisted.python.logfile import DailyLogFile
from twisted.python import usage, log

class Options(usage.Options):

    optParameters = [
        ["logfile", "l", "twisted.log", "Where to put logs"],
        ["reactor", "r", "select", "Nuclear plant type"],
        ["config", "c", "config.json", "Where are the settings lies"]
    ]

def initLogs(logDest):
    try:
        if logDest == 'syslog':
            syslog.startLogging('app')
        elif logDest == 'stdout':
            log.startLogging(sys.stdout)
        else:
            log.startLogging(DailyLogFile(os.path.basename(logDest), os.path.dirname(logDest)))
    except Exception, ex:
        log.startLogging(sys.stdout)
        log.msg(str(ex))

def installReactor(rtype):
    if rtype == 'epoll':
        from twisted.internet import epollreactor
        epollreactor.install()

def loadConfig(conf):
    config = ConfigParser.ConfigParser()
    config.read(conf)
