__author__ = 'MrJew'


from configuration import Configuration
from populator import Populator

from baseConfig import BaseConfig
import operator
import math

class Config(BaseConfig):

    def mul(self,a,b):
        return operator.mul(a,b)

    def add(self,a,b):
        return operator.add(a,b)

    def saveDiv(self,a,b):
        if b==0:
            return 0
        else:
            return a/b

    def subtract(self,a,b):
        return operator.sub(a,b)

    def fitnessFunction(self,x):
        return x**3+x**2-8


arguments = {"x":[0,1,-5,12,100,-3.0,-2,45.1]}
c = Configuration(configClass=Config(),numberOfArgs=1,pop=1000,gen=40,cx=0.9,cloud="http://127.0.0.1:8888",arguments=arguments)
c.pset.renameArguments(ARG0="x")
c.setTerminal(1)
c.configure()
p = Populator(c)
p.populate()
