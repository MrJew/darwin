__author__ = 'MrJew'

import cherrypy

########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': 'localhost',	    #
                        'server.socket_port': 8080,				#
                       })										#
#################################################################

class CopyService():

    def index(self,x,y,z):
        r = (float(x)+1)**2 + float(y)*float(z)*4 - 3*float(x)
        return str(r)

    index.exposed = True

cherrypy.quickstart(CopyService())


