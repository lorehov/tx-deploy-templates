from twisted.python import usage


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

