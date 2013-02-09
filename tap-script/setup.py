#!/usr/bin/env python
import twisted
from distutils.core import setup

def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

dist = setup(
    name='mservice',
    version='0.1',
    description = "mservice",
    author="PVI",
    author_email="pvi@gmail.com",
    url="ssh://git@mservice.git",
    license="GPL",

    packages=['mservice', 'twisted.plugins'],
    package_data = {
        'twisted': ['plugins/service_plugin.py']
    },
    scripts=['mt4emulator'],
    data_files=[('/usr/bin',['bin/mt4emud'])]
)

refresh_plugin_cache()