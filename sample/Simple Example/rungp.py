__author__ = 'mrjew'
from darwin.runner import *
from darwin.primitiveConfig import *

p= runGP( xmlConfig="config.xml")
print p.hof[0]
p.generateWebService(p.hof[0])








