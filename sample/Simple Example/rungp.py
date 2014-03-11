__author__ = 'mrjew'
from runner import *


p = runGP(xmlConfig="config.xml")
print p.hof[0]
p.generateWebService(p.hof[0])