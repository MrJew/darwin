from deap import base,creator,gp,tools

class Configuration:
    toolbox = base.Toolbox()
    pset = None
    listOfFintes = []
    configClass = None
    arguments = None
    cloud = None
    copyService = None
    isMax = False
    pop,gen,cx,mut = 100,40,0.1,0.5
    depthInitialMin = 1
    depthInitialMax = 3
    maxDepthLimit = 17


    def __init__ (self ,configClass ,testArguments=None ,pop=None ,gen=None, cx=None, mut=None,
                  evaluatingService=None,copyService=None,depthInitialMin=None,
                  depthInitialMax=None,isMax=None,maxDepthLimit=None):

        self.configClass = configClass
        self.cloud = evaluatingService
        self.copyService = copyService
        self.testArguments = testArguments

        if pop      : self.pop = pop
        if gen      : self.gen = gen
        if depthInitialMax : self.deptInitialMax = depthInitialMax
        if depthInitialMin : self.deptInitialhMin = depthInitialMin
        if isMax    : self.isMax = isMax
        if maxDepthLimit : self.maxDepthLimit = maxDepthLimit

        if mut and mut<1 and mut>0 : self.mut = mut
        if cx and cx<1 and cx>0 : self.cx = cx

        self.pset = gp.PrimitiveSet("MAIN", len(testArguments))


    def setPrimitiveFunctions(self):
        for function in self.configClass.getFunctions():
            self.pset.addPrimitive(function[0],function[1])

    def addIndividualArguments(self,argument):
        self.pset.renameArguments(ARG0=argument)

    def getFitnessFunction(self):
        return (getattr(self.configClass,"fitnessFunction"))

    def configure(self):
        self.setPrimitiveFunctions()

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
        renameArgs = {}
        argNames = list(enumerate(self.testArguments.keys()))

        for entry in argNames:
            renameArgs["ARG"+str(entry[0])] = entry[1]
        self.pset.renameArguments(**renameArgs)

    def setEmpheralConstant(self,constant):
        self.pset.addEphemeralConstant(constant)

    def setTerminal(self, terminal):
        if isinstance( terminal, (float,int,long) ): self.pset.addTerminal(terminal)
        else:
            for i in terminal: self.pset.addTerminal(i)

    # Setters for the configurations

    def setCopyService(self, copyService):
        self.copyService = copyService

    def setEvaluatingService(self, evaluatingService):
        self.cloud = evaluatingService

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
