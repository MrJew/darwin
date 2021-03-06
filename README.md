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
 

Darwin is a genetic programming framework for cloning web services. It aims to give the user only the
necessary functionality for revere engineering the functionality of a web service while automating the rest of 
the process. It is using the DEAP framework for genetic programming so some of the configurations are
similar. Darwin focuses on simplicity so it provides a GUI for generating the configuration file needed for the framework. This tutorial explains how to use the framework, both basic and advanced
examples are provided which are located in the project folder.

Dependencies
=================================================================================================
Packages required for the system to run besides Python 2.7.

1. DEAP 0.9.2 - http://deap.gel.ulaval.ca/doc/0.9/index.html
2. requests 2.3 - http://docs.python-requests.org/en/latest/
3. CherryPy 3.2 - http://www.cherrypy.org/
4. pygraphviz 1.2 - http://pygraphviz.github.io/
5. wxpython 2.9 - https://pypi.python.org/pypi/wxPython/2.9.1.1
6. lxml - 3.1.2 - http://lxml.de/installation.html

Make sure that all the libraries and the darwin python package are in your python path when
you are running the examples.

Basic Example
=================================================================================================
In the /examples folder are located the examples for the framework. To demonstrate the basic functionality
we will use the files in /examples/Simple Example:

If you want to try the cloning example:

1. Run the Evaluator - cherrypyinstance.py
2. Run the service we are cloning - dummyinstance.py 
3. Run the Client - rungp.py *needs to be ran last*.

What we get is the best individual at clonedwebservice.py . The web service generated based on the primitive set.

Let's try this. 

1. In rungp.py import primitiveConfig
2. create a class that extends PrimitiveConfig
3. write a method with the name "targetFunction(self, args...) and give it a return statement. The framework will automatically assign the arguments to the method based on the arguments given from the .csv file names "args.csv".
Darwin will later use the target function to calculate the fitness.

    def targetFunction(self,x,y,z):

4. After the function is created we need to provide an XML file configuration file. Run the GUI located in darwin/UI.py, there you can choose among multiple configuration options. Since we want to use a targetFunction() rather than a URL address we leave Target URL field empty. Then you'll need to choose the primitives from the checkbox to the left. Primitives are the functions the framework is going to use in order to clone your expression. In the arguments field a path to the .csv file needs to be specified where the test arguments are defined the format looks like this:

*NOTE*: The name of the arguments in the .csv file need to be the same as the arguments in your target function.

    x,1.0,2,3.1,-4
    y,8.3,-22,3.1,-4
    z,2.0,1,-8.1,-4
    
In the end the Terminals are defined which are the constants that you want to be used in your evaluation for example if the targetFunction is measuring the size of a circle pi would be required as a terminal. Sperate multiple terminals with comma. For example if expression is:

    return x + y + z/3

Then 3 will be terminal.

Click "Generate" to save the XML file in a location of your choice

5. Call configuration parsing as parameter the newly created config class and your XML config file.

For example:

    class Config(PrimitiveConfig):

        def targetFunction(self,x,y,z):
            return x + y + z/3

    runGP(configClass=Config(),xmlConfig="config.xml")

Where "config.xml" is the location of the configuration XML you want to use.

6.There are two ways to configure the framework, one is through the XML file as shown above and the other one is through the code with expressions. To do that we need to work with the configuration and population class directly like this as shown below. Change the code in rungp with this:

    c = Configuration(configXml="config.xml")
    c.setTargetService("http://localhost:8080") # if you run dummyInstance that's the url to access it
    c.setEvaluatingService("http://localhost:8844") # if you run cherryInstance that's the url to access it
    c.pop = 1000 # define the population
    c.gen = 1000 # define the generations
    p = Populator(configuration=c)
    p.populate()
    
This code will set the evaluating service which mean it will not run your targetFunction as a fitness but rather what the web service located at "http://localhost:8844" returns. This web service can be ran through dummyInstance.py . You can try applying the same expression you used in the targetFunction in the service.

    class CopyService():

        def index(self,x,y,z):
            x,y,z = float(x),float(y),float(z)
            r = x+y+z
            return str(r)

        index.exposed = True
    
Simply substitute "r" with the expression of your choice.

*NOTE:* dummyinstance.py is runing at http://localhost:8080 and cherrypyinstace.py at http://localhost:8844

Congratulations  you just used Darwin framework to clone a web service.


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
Let's cloning a real web service. A good example for a web service to
clone is Wolfram Alpha. However we need to construct the URL for Wolfram Alpha this is done through
requestHandler and later on the XML response needs to be handled by responseHandler. For example:

    class Config(PrimitiveConfig):

        # targetServiceURL = http://api.wolframalpha.com/v2/query
        # params are defined in the .csv file in WolframAlpha folder 
        def requestHandler(self,url,testArguments):
            apid= "X63LWT-U7E9YX8R2K"
            formatw = "plaintext"
            expression="pi*("+str(testArguments['r'])+"%5E2)"
            arguments = {'format':formatw,'input':expression,'appid':apid}
            return self.handler(main,params=arguments)

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
        
"params" is a dictionary that contains a single set of test arguments. If we have arguments x,y,z
and we have a csv file in the form

    x,1,2,3,4
    y,1,2,3,4
    z,1,2,3,4
   
"params" in requestHandler is going to be {'x':1,'y':1,'z',1}. In our case the only argument is being
'r' . Which in the case of the example take arguments:

    r,1,0,1.5,5,15,13.4,10,32

We return with a call to self.hadler that can take up to two arguments an url and a dictionaries with URL paramters.
In the case of WolframAlpha parameters to the url http://api.wolframalpha.com/v2/query are appid,format,input.

In the responseHandler we are handling the XML reposne received from Wolfram Alpha and the result we
are interested in is written to the variable 'result'. It's up to us to convert the result in string
form to float so a fitness value for the set of parameters can be returned.


