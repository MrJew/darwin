Darwin
=================================================================================================
                                                                                
                                                                       . :.           MMMO          
                                                                .M,    MMMM.         .MMMM          
                                                                   .M OMMMM.         MMMMN          
                                                       .NMMN,         MMMN         .MMMM            
                                            :MM:       MMMMM.        MMMM :MN.     .MMMMM           
                                            MMMM.     MMMMM          MMMMMN N,M    .MMMMM.          
                                         ,MMM:,      .MMMMM          MMMMMMM.      MMMMMM,          
                                         MMMMN.       MMMMM         .MMMMMMN       MMMMMMMMMN,      
                                        DMMMMM.      MMMMMM         .MMMMM..       MMMMMM    M      
                                MMMM,  OMMMMMMMM,     MMMM:M.       NMMMMM.        MMMMM.           
                            .MMMMMMMM  MMMMMM   DM.  MMMMM .M.      .MMMMM        .MMMMMM.          
                           NMMMMMM      MMMM,   .N   ~MMM.  .M       :MMMM.        MMMNMMM.         
                         ,MMMMMMM.     :MMMMM?.       MMMM .MN       MMMMM:        ,MM  MMM         
                        OMMMMMMMM       NMM.MMM.     ,MMMMM          NMMNMM        MMD   MMM        
                        MMMMMMMMMM       MM .MMM     NMN .MD        MMM ~MM.      MMM.   .MM.       
                          MMMMM,NM       NM  MM.    MMM   MM.      MM, .MMM     .MM       MMM       
                        :MMMOMM..M.  ~MMMMN. MM.  .MM,    MM.    MM..   .MM     ,M        .MM.      
                      ,MMD,  MM  .N  MN      MM   .M.     ,M.   ,MM      MM     M8          MMMNM   
                      ~M.   .MMM.ND  MM.     MMMM  MM.     MMMM. .MM     NMMNM. ,MMD,       ,M..    
 

Darwin is a genetic programming framework for clonning web services. It aims to give the user only the
necessary functionality for reversing the functionality of a web service while automating the rest of 
the process. It is using the DEAP framework for genetic programming so some of the configurations are
simmilar. Darwin focuses on simplicity so it provides a GUI for generating the configuration file needed for the framework. In the following tutorial you will be explained how to use the framework, bot basic and advanced
examples are provided which are located in the project folder.

Dependencies
=================================================================================================
Packages required for the system to run.

DEAP
requests
CherryPy
pygraphvz
inspect
wxpython

Basic Example
=================================================================================================
In the /examples folder are located the examples for the framework. To demonstrate the basic functionality
we will use the files in /Simple Example:

If you want to try the cloning example:

1. Run the Evaluator - cherrypyinstance.py
2. Run the service we are clonning - dummyinstance.py 
3. Run the Client - rungp.py *needs to be ran last*.

What we get is the best individual and at clonedwebservice.py . The web service generated based on the primitive set.

Let's try this. 

1. In rungp.py import primitiveConfig
2. create a class that extends PrimitiveConfig
3. write a method with the name "targetFunction(self, args...) and give it a return statement. The framework will automatically assign the arguments to the method based on the arguments given from the .csv file names "args.csv".
Darwin will later use the target function to calculate the fitness.
4. After the function is created we need to provide an XNL file configuration file. Run the GUI located in gui folder there you can choose among multiple configuration options. Since we want to use a targetFunction() rather than a URL address we leave Target URL field empty. Then you'll need to choose the primitives from the checkbox to the left. Primitives are the functions the framework is going to use in order to clone your expression. In this case we know the expression so we should use primitives that are going to be used in the expression. However normally we will need to assume what the primitives can be. In the arguments field a path to the .csv file needs to be specified where the test arguments are defined the format looks like this:

    x,1.0,2,3.1,-4
    y,8.3,-22,3.1,-4
    z,2.0,1,-8.1,-4
    
In the end the Terminals are defined which are the constants that you want to be used in your evaluation for example if the targetFunction is measuring the size of a circle pi would be required as a terminal. Click "Generate" to save the XML file in a location of your choice
5. Call configuration parsing as parameter the newly created config class and your XML config file.

For example:

    class Config(PrimitiveConfig):

        def fitnessFunction(self,x,y,z):
            return x + y + z/3

    runGP(configClass=Config(),configXml="config.xml")

Where "config.xml" is the location of the configuration XML you want to use.

6.There are two ways to configure the framework, one is through the XML file as shown above and the other one is through the code with expressions. What runGP does is

    def runGP(xmlConfig=None,configClass=None):
    c = Configuration(configClass=configClass,configXml="config.xml")
    c.configure()
    p = Populator(configuration=c)
    p.populate()
    return p
    
However this does not give us the opportunity to dinamically configure the framework. To do that we need to work with the configuration and population class directly like this as shown below:

    c = Configuration(configXml="config.xml")
    c.setTargetService("http://localhost:8080") # if you run dummyInstance that's the url to access it
    c.setEvaluatingService("http://localhost:8844") # if you run cherryInstance that's the url to access it
    c.pop = 1000 # define the population
    c.gen = 1000 # define the generations
    
This code will set the evaluating service which mean it will not run your targetFunction as a fitness but rather what the web service located at "http://localhost:8844" returns. This web service can be ran through dummyInstance.py . You can try applying the same expression you used in the targetFunction in the service.

    class CopyService():

    def index(self,x,y,z):
        x,y,z = float(x),float(y),float(z)
        r = x+y+z
        return str(r)

    index.exposed = True
    
Simply substitute "r" with the expression of your choice.

Congradulations you just used Darwin framework to clone a web service.


Advanced Example
=================================================================================================
Custom Primitives:
In more advance cases you would want to configure the framework yourself. You might want to activate
special features or set certain parameters. For example the baseic set of primitives might not be good enough
and you need additional ones. What you need to do is simply extend PrimitiveConfig.

For example:

    class Config(PrimitiveConfig):
    
        def myComplextMath(self,x,y,z):
            return x + y - z*2 - 1

        def specialMathFunction(self,a,b,c):
            return a*b*(c-1)
            
    c = Configuration(configClass=Config(),configXml="config.xml")
    c.configure()
    p = Populator(configuration=c)
    p.populate()
    
The way PrimitiveConfig works is except the methods ["listOfExcludes","getSource","getPrimitives","functionArgs","updateExcludes",
                      "targetFunction","numberOfFunctionArgs","getFunctions","basicPrimitives"
                      ,"requestHandler","responseHandler", "handler",]
every other method name is generating a primitive for the framework to use.
Update the basic example to use primitive sets that you've created. If you've chosen an expression
that can use those primitives you will see them in the final individual.

Clone Wolfram Alfa Example
=================================================================================================
Let's try cloning a real web service not one generated by us. A good example for a web service to
clone is Wolfram Alpha. However we need to construct the URL for Wolfram Alpha this is done through
requestHandler and later on the XML response needs to be handled by responseHandler. For example:

    class Config(PrimitiveConfig):

    # targetServiceURL = http://api.wolframalpha.com/v2/query
    # params are defined in the .csv file in WolframAlpha folder 
    def requestHandler(self,url,params):
        apid= "X63LWT-U7E9YX8R2K"
        exp = "pi*("+str(params['r'])+"%5E2)"   # pi*r^2
        main = url+"?appid="+apid+"&input="+exp+"&format=plaintext"
        return self.handler(main)

    def responseHandler(self,r):
        r.encoding = 'ASCII'
        xml = r.text
        xml = '\n'.join(xml.split('\n')[1:])
        root = etree.fromstring(xml)
        result = ''
        for pod in root.findall('.//pod'):
            for pt in pod.findall('.//plaintext'):
                if pt.text and pod.attrib['title'] == 'Result':
                    result = pt.text

        if "..." in result:
            result = result[:-3]
        return float(result)
        
params is a dictionary that contains a single set of test arguments. If we have arguments x,y,z
and we have a csv file in the form

    x,1,2,3,4
    y,1,2,3,4
    z,1,2,3,4
   
params in requestHandler is going to be {'x':1,'y':1,'z',1}. In our case the only argument is being
'r' .

In the responseHandler we are handling the xml reposne received from Wolfram Alpha and the result we
are interested in is written to the variable 'result'. It's up to us to convert the result in string
form to float so a fitness value for the set of parameters can be returned.


