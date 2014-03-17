__author__ = 'MrJew'
from darwin.baseCherryPy import BaseCherryPy
import cherrypy


########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': 'localhost',	#
                        'server.socket_port': 8844,				#
                       })										#
#################################################################


class HelloWorld(BaseCherryPy):

    def index(self):
        return "Hello world!"
    index.exposed = True


cherrypy.quickstart(HelloWorld())
