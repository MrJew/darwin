from baseCherryPy import BaseCherryPy
import sys
import operator
import math
import cherrypy

########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': '',	
                    'server.socket_port': 8844,})				
#################################################################

class ClonedWebService(BaseCherryPy):

    def mul(self,a,b):
        return operator.mul(a,b)

    def pow(self,a,b):
        try:
            return math.pow(a,b)
        except:
            return 0

    def main(self,r):
        r = float(r)
        ind = lambda r: self.mul(self.mul(3.14, r), r)
        return ind(r)

    def index(self,r):
        return self.main(r)
    index.exposed = True

cherrypy.quickstart(ClonedWebService())