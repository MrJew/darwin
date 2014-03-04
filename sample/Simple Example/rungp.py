__author__ = 'mrjew'
from runner import *
from primitiveConfig import *


p = runGP(xmlConfig="config.xml")
p.generateWebService(p.hof[0])