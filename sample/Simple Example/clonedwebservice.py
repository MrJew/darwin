from baseCherryPy import BaseCherryPy
import sys
import math
import operator
import cherrypy

########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': '',	
                    'server.socket_port': 8844,})				
#################################################################

class ClonedWebService(BaseCherryPy):

    def add(self,a,b):
        return operator.add(a,b)

    def mul(self,a,b):
        return operator.mul(a,b)

    def safeDiv(self,a,b):
        if b==0:
            return 0
        else:
            return operator.div(a,b)

    def sub(self,a,b):
        return operator.sub(a,b)

    def main(self,y,x,z):
        y = float(y)
        x = float(x)
        z = float(z)
        ind = lambda y,x,z: self.add(x, self.add(y, z))
        return ind(y,x,z)

    def index(self,y,x,z):
        return self.main(y,x,z)
    index.exposed = True

cherrypy.quickstart(ClonedWebService())