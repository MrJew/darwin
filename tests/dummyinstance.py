__author__ = 'MrJew'

import cherrypy
import inspect

########################### CONFIG ##############################
cherrypy.config.update({'server.socket_host': '192.168.0.111',	    #
                        'server.socket_port': 8080,				#
                       })										#
#################################################################

class CopyService():

    def index(self,x,y,z):
        if float(z)!=0:
            r = float(x)**2 + float(y)/float(z) - 3
        else: r = float(x)**2 - 3
        print r
        return str(r)

    index.exposed = True

cherrypy.quickstart(CopyService())


