from deap import base,creator,gp,tools
from lxml import etree
import StringIO
from baseConfig import *

class Configuration:
    """
        Configuration sets all thee needed parameters for the GP and then is transferred
        over a network to the evaluating web service
        *configClass*       : based on the class the primitive functions are set
        *testArguments*     : in the form of list of dictinaries give the arguments
        that are going to be tested on the individuals and the service that is copied
        the name of the arguments must match the ones it the primitive function
        *evaluatingService* : url to the service that is going to be evaluating the individuals
        *pop*               : size of the population for each generation
        *gen*               : number of generations
        *cx*                : crossing rate over the population, value must be between 0.0 - 1.0 (0.5)
        *mut*               : mutation rate over the population, value must be between 0.0 - 1.0 (0.1)
        *copyService*       : url to the service or API we are copying
        *depthInitialMin*   : the depth of the initially generated individuals (1-3)
        *isMax*             : sets the type of the fitness function to min or max (min)
        *maxDepthLimit*     : sets the maximum depth of the individual tree (17)
        *logging*           : if true logging is enabled
        *hofnum*            : number of best individuals saved
    """
    toolbox = base.Toolbox()
    pset = None
    listOfFintes = []
    configClass = None
    arguments = None
    evalUrl = None
    copyUtl = None
    isMax = False
    pop,gen = 1000,40
    cx,mut = 0.1,0.5
    depthInitialMin = 1
    depthInitialMax = 3
    maxDepthLimit = 17
    logging = True
    hofnum = None
    imports = []
    terminals = []


    def __init__ (self, configClass=None, configXml=None, testArguments=None,evaluatingService=None, pop=None, gen=None, cx=None, mut=None,
                  copyService=None, depthInitialMin=None, hofnum=None, imports=None,
                  depthInitialMax=None, isMax=None, maxDepthLimit=None, logging=None):

        if configClass : self.configClass = configClass
        else: self.configClass = BaseConfig()
        self.evalUrl = evaluatingService
        self.copyUrl = copyService
        self.testArguments = testArguments
        if imports  : self.imports = imports
        if pop      : self.pop = pop
        if gen      : self.gen = gen
        if hofnum   : self.hofnum = hofnum
        if isMax    : self.isMax = isMax
        if logging  : self.logging = logging
        if depthInitialMax : self.deptInitialMax = depthInitialMax
        if depthInitialMin : self.deptInitialhMin = depthInitialMin
        if maxDepthLimit : self.maxDepthLimit = maxDepthLimit
        if mut and mut<1 and mut>0 : self.mut = mut
        if cx and cx<1 and cx>0 : self.cx = cx

        if configXml : self.configXml(configXml)


        self.pset = gp.PrimitiveSet("MAIN", len(self.testArguments))

    def configXml(self,xmlFile):
        """ Configure the gp framework through an xml file specifying the parameters"""

        tree = etree.parse("../"+xmlFile)
        root = tree.getroot()
        children = []
        params = {}

        for child in root:
            children.append(child.tag)

        for child in children:
            if child == "import":
                params[child] = root.find(child).text.split(",")
            else:
                params[child] = root.find(child).text

        if params['cx']     : self.cx = float(params['cx'])
        if params['mut']    : self.mut = float(params['mut'])
        if params['pop']    : self.pop = int(params['pop'])
        if params['gen']    : self.gen = int(params['gen'])
        if params['import']: self.imports = params['import']
        if params['evalUrl']: self.evalUrl = params['evalUrl']
        if params['copyUrl']: self.copyUrl = params['copyUrl']
        if params['args']   : self.testArguments = eval(params['args'])
        if params['basicPrimitives'] : self.configClass.updateExcludes(eval(params['basicPrimitives']))
        if params['terminals']       : self.terminals = eval(params['terminals'])


    def setPrimitiveFunctions(self):
        """ Sets the primitive function set based on the configuration class you give it"""
        for function in self.configClass.getFunctions():
            self.pset.addPrimitive(function[0],function[1])

    def getFitnessFunction(self):
        """ Returns an instance of the fitness function"""
        return (getattr(self.configClass,"fitnessFunction"))

    def configure(self):
        """ Creates the toolbox and sets all the needed parameters"""
        self.setPrimitiveFunctions()
        self.setTerminals(self.terminals)

        if not self.isMax   : creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        else                : creator.create("FitnessMax", base.Fitness, weights=(-1.0,))

        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=self.pset)
        self.toolbox.register("expr", gp.genRamped, pset= self.pset, min_=self.depthInitialMin, max_=self.depthInitialMax)
        self.toolbox.register("individual", tools.initIterate, creator.Individual,  self.toolbox.expr)
        self.toolbox.register("population", tools.initRepeat, list,  self.toolbox.individual)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register('mutate', gp.mutUniform, expr= self.toolbox.expr_mut)

        self.toolbox.decorate('mutate',gp.staticDepthLimit(self.maxDepthLimit))
        self.toolbox.decorate('mate',gp.staticDepthLimit(self.maxDepthLimit))
        self.configureArguments()

    def configureArguments(self):
        """ Based on the fitness function it sets the arguments for the GP """
        renameArgs = {}
        argNames = list(enumerate(self.testArguments.keys()))

        for entry in argNames:
            renameArgs["ARG"+str(entry[0])] = entry[1]
        self.pset.renameArguments(**renameArgs)

    def setEmpheralConstant(self,constant):
        self.pset.addEphemeralConstant(constant)



    def setTerminals(self, terminal):
        """ terminal: either a list or a numerical constant """
        if isinstance( terminal, (float,int,long) ): self.pset.addTerminal(terminal)
        else:
            for i in terminal: self.pset.addTerminal(i)

    # Setters for the configurations

    def setCopyService(self, copyService):
        self.copyUrl = copyService

    def setEvaluatingService(self, evaluatingService):
        self.evalUrl = evaluatingService

    def setConfig(self,configClass):
        self.configClass = configClass

    def setArguments(self, argList):
        self.arguments = argList

    def setFitnessMax(self,isMax):
        self.isMax=isMax

    def setMinInitialDepth(self,depthlvl):
        self.depthMin = depthlvl

    def setMaxInitialDepth(self,depthlvl):
        self.depthMax = depthlvl

    def setMaxDepthLimit(self,maxDepthLimit):
        self.maxDepthLimit = maxDepthLimit
