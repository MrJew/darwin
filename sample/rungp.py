__author__ = 'mrjew'
from runner import *
from primitiveConfig import *


p = runGP(xmlConfig="config.xml")
p.draw(p.hof[0],"individual1.png")
p.draw(p.hof[1],"individual2.png")
p.draw(p.hof[2],"individual3.png")
p.draw(p.hof[3],"individual4.png")