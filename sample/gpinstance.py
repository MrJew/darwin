__author__ = 'MrJew'


from configuration import Configuration
from baseConfig import BaseConfig
from populator import *

class Config(BaseConfig):

    def mul(self,a,b):
        return operator.mul(a,b)

    def add(self,a,b):
        return operator.add(a,b)

    def saveDiv(self,a,b):
        if b==0:
            return 0
        else:
            return a/b

    def subtract(self,a,b):
        return operator.sub(a,b)


arguments = {"x":[0,1,-5,12,100,-3.0,-2,45.1],
             "y":[0,1,-5,12,100,-3.0,-2,45.1],
             "z":[0,1,-5,12,100,-3.0,-2,45.1]}

imports = ["operator"]

#c = Configuration(configClass=Config(),pop=1000,gen=100,cx=0.9,mut=0.1,maxDepthLimit=10,
#                  evaluatingService="http://localhost:8844",
#                  copyService="http://localhost:8080",testArguments=arguments,imports=imports)
c = Configuration(Config(),configXml="config.xml")
c.setTerminal(1)
c.configure()
p = Populator(configuration=c)
p.populate()

