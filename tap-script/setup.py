#!/usr/bin/env python
import twisted
from distutils.core import setup

def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

dist = setup(
    name='mserv',
    version='0.1',
    description = "mserv",
    author="PVI",
    author_email="pvi@gmail.com",
    url="ssh://git@mserv.git",
    license="GPL",

    packages=['mserv', 'twisted.plugins'],
    package_data = {
        'twisted': ['plugins/service_plugin.py']
    },
    scripts=['mt4emulator'],
    data_files=[('/usr/bin',['bin/mt4emud'])]
)

refresh_plugin_cache()