__author__ = 'MrJew'

import cherrypy
import os
from functionCatcher import FunctionIOCatcher

class BaseCherryPy:
    configuration = None
    _cp_config = {'tools.inputCatcher.on': True,'tools.outputCatcher.on': True}

    def __init__(self,configuration,fname):
        self.configuration = configuration


    def lambdify(self,expr, pset):
        args = ",".join(arg for arg in pset.arguments)
        lstr = "lambda {args}: {code}".format(args=args, code=expr)
        return eval(lstr, dict(pset.context))

    def inputCatcher(self=None):
        params = cherrypy.request.params['logfile']
        functionCatcher = FunctionIOCatcher(str(params),"evaluate")
        functionCatcher.catchInput(cherrypy.request.params)
        print "after"

    def outputCatcher(self=None):
        params = cherrypy.request.params['logfile']
        functionCatcher = FunctionIOCatcher(str(params),"evaluate")
        functionCatcher.catchOutput(cherrypy.response.body)

    def evaluate(self,individual,arguments,logfile=None):
        arguments = eval(arguments)
        newArgs=[]
        for i in range(len(arguments.values()[0])):
            nd={}
            for key in arguments.keys():
                nd[key]=arguments[key][i]
            newArgs.append(nd)


        func = self.lambdify(individual,self.configuration.pset)
        fitness = self.configuration.getFitnessFunction()
        diff=0
        for i in newArgs:
            diff += (func(**i) - fitness(**i))**2

        return str(diff)

    evaluate.exposed=True

    cherrypy.tools.inputCatcher = cherrypy.Tool('before_handler', inputCatcher)
    cherrypy.tools.outputCatcher = cherrypy.Tool('before_finalize', outputCatcher)





