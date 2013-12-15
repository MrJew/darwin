from deap import base,creator,gp,tools

class Configuration:
    pop,gen,cx,mut = 100,40,0.1,0.5
    toolbox = base.Toolbox()
    pset = None
    listOfFintes = []
    configClass = None
    arguments = None
    cloud = None
    isMax = False
    depthMin = 1
    depthMax = 3

    def __init__ (self,configClass,numberOfArgs,arguments=None,pop=None,gen=None,cx=None,mut=None, cloud=None,depthMin=None,depthMax=None,isMax=None,):
        self.pset = gp.PrimitiveSet("MAIN", numberOfArgs)

        self.configClass = configClass
        self.cloud = cloud
        self.testArguments = arguments

        if pop      : self.pop = pop
        if gen      : self.gen = gen
        if depthMax : self.depthMax = depthMax
        if depthMin : self.depthMin = depthMin
        if isMax    : self.isMax = isMax

        if mut and mut<1 and mut>0 : self.mut = mut
        if cx and cx<1 and cx>0 : self.cx = cx

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
        self.toolbox.register("expr", gp.genRamped, pset= self.pset, min_=self.depthMin, max_=self.depthMax)
        self.toolbox.register("individual", tools.initIterate, creator.Individual,  self.toolbox.expr)
        self.toolbox.register("population", tools.initRepeat, list,  self.toolbox.individual)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register('mutate', gp.mutUniform, expr= self.toolbox.expr_mut)

    def setEmpheralConstant(self,constant):
        self.pset.addEphemeralConstant(constant)

    def setTerminal(self, terminal):
        if isinstance( terminal, (float,int,long) ): self.pset.addTerminal(terminal)
        else:
            for i in terminal: self.pset.addTerminal(i)

    def setCloud(self, cloud):
        self.cloud = cloud

    def setConfig(self,configClass):
        self.configClass = configClass

    def setArguments(self, argList):
        self.arguments = argList

    def setFitnessMax(self,isMax):
        self.isMax=isMax

    def setMinDepth(self,depthlvl):
        self.depthMin = depthlvl

    def setMaxDepth(self,depthlvl):
        self.depthMax = depthlvl