__author__ = 'MrJew'

import cherrypy

########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': 'localhost',	    #
                        'server.socket_port': 8080,				#
                       })										#
#################################################################

class CopyService():

    def index(self,x,y,z):
        x,y,z = float(x),float(y),float(z)
        r = x+y+z
        return str(r)

    index.exposed = True

cherrypy.quickstart(CopyService())


