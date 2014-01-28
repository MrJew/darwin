__author__ = 'mrjew'
from configuration import Configuration
from populator import Populator

def runGP(xmlConfig=None,configClass=None):
    c = Configuration(configClass=configClass,configXml="config.xml")
    c.configure()
    p = Populator(configuration=c)
    p.populate()