__author__ = 'MrJew'

from configuration import Configuration
from baseCherryPy import BaseCherryPy
from baseConfig import BaseConfig
import operator
import cherrypy


########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': '127.0.0.1',	#
                        'server.socket_port': 8888,				#
                       })										#
#################################################################

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


class HelloWorld(BaseCherryPy):

    def index(self):
        return "Hello world!"
    index.exposed = True


c = Configuration(configClass=Config(),numberOfArgs=1)
c.pset.renameArguments(ARG0="x")
c.setTerminal(1)
c.configure()
cherrypy.quickstart(HelloWorld(c,fname="log.txt"))

