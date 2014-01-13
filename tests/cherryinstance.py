__author__ = 'MrJew'

from configuration import Configuration
from baseCherryPy import BaseCherryPy
from baseConfig import BaseConfig
import operator
import cherrypy


########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': 'localhost',	#
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


class HelloWorld(BaseCherryPy):

    def index(self):
        return "Hello world!"
    index.exposed = True

arguments = {"x":[0,1,-5,12,100,-3.0,-2,45.1],
             "y":[0,1,-5,12,100,-3.0,-2,45.1],
             "z":[0,1,-5,12,100,-3.0,-2,45.1]}


c = Configuration(configClass=Config(),testArguments=arguments,maxDepthLimit=10)
c.setTerminal(1)
c.configure()
cherrypy.quickstart(HelloWorld(c))
