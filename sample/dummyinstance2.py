__author__ = 'MrJew'

import cherrypy

########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': 'localhost',	    #
                        'server.socket_port': 8082,				#
                       })										#
#################################################################

class CopyService():

    def index(self,x,y,z):
        r = float(x)
        return str(r)

    index.exposed = True

cherrypy.quickstart(CopyService())


