__author__ = 'MrJew'

from darwin.baseCherryPy import BaseCherryPy
import cherrypy


########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': 'localhost',	#
                        'server.socket_port': 8844,				#
                       })										#
#################################################################


class HelloWorld(BaseCherryPy):

    def hello(self):
        return "Hello world!"
    hello.exposed = True


cherrypy.quickstart(HelloWorld())
