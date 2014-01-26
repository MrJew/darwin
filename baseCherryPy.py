__author__ = 'MrJew'

import sys
from helper import stdoutIO

class BaseCherryPy:


    def evaluateCopy(self,individual,arguments):
        arguments = eval(arguments)
        diff=0

        for i in arguments:
            sys.argv = i[0]
            print individual
            with stdoutIO() as s:
                exec(individual) in {}
            diff += (float(s.getvalue()) - i[1])**2
        return str(diff)

    evaluateCopy.exposed=True






