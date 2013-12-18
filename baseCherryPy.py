__author__ = 'MrJew'

import cherrypy
from functionCatcher import FunctionIOCatcher
from helper import *

class BaseCherryPy:
    configuration = None
    _cp_config = {'tools.inputCatcher.on': True,'tools.outputCatcher.on': True}

    def __init__(self,configuration):
        self.configuration = configuration

    def lambdify(self,expr, pset):
        args = ",".join(arg for arg in pset.arguments)
        lstr = "lambda {args}: {code}".format(args=args, code=expr)
        return eval(lstr, dict(pset.context))

    def inputCatcher(self=None):
        params = cherrypy.request.params['logfile']
        functionCatcher = FunctionIOCatcher(str(params),"evaluate")
        functionCatcher.catchInput(cherrypy.request.params)

    def outputCatcher(self=None):
        params = cherrypy.request.params['logfile']
        functionCatcher = FunctionIOCatcher(str(params),"evaluate")
        functionCatcher.catchOutput(cherrypy.response.body)

    def evaluate(self,individual,arguments,logfile=None):
        arguments = eval(arguments)
        newArgs = listTokwags(arguments)
        func = self.lambdify(individual,self.configuration.pset)
        fitness = self.configuration.getFitnessFunction()
        diff=0
        for i in newArgs:
            diff += (func(**i) - fitness(**i))**2
        return str(diff)

    evaluate.exposed=True

    def evaluateCopy(self,individual,arguments,logfile=None):
        arguments = eval(arguments)
        func = self.lambdify(individual,self.configuration.pset)
        diff=0
        for i in arguments:
            diff += (func(**i[0]) - i[1])**2
        return str(diff)

    evaluateCopy.exposed=True

    cherrypy.tools.inputCatcher = cherrypy.Tool('before_handler', inputCatcher)
    cherrypy.tools.outputCatcher = cherrypy.Tool('before_finalize', outputCatcher)





