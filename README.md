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
 

Basic Example
=================================================================================================
In the /sample folder are located the examples for the Client, evalator and the cloning instance. 

If you want to try the cloning example:

1. Run the Evaluator - cherrypyinstance.py
2. Run the service we are clonning - dummyinstance.py 
3. Run the Client - rungp.py *needs to be ran last*.

If you want to run only the evaluator and use your own fitness function

1. In rungp.py import baseConfig
2. create a class that extends PrimitiveConfig
3. write a method with the name "fitnessFunction(self, args...) and give it a return statement
4. call configuration parsing as parameter the newly created config class and your xml config file (use the template)

For example:

    class Config(PrimitiveConfig):

        def fitnessFunction(self,x,y,z):
            return x + y + z/3

    c = Configuration(configClass=Config(),configXml="config.xml")
    c.configure()
    p = Populator(configuration=c)
    p.populate()

Where "config.xml" is the location of the configuration XML you want to use.
There are two ways to configure the framework through the code  with expressions
like
    
    c = Configuration()
    c.setTargetService("http://localhost:8080") # if you run dummyInstance that's the url to access it
    c.setEvaluatingService("http://localhost:8844") # if you run cherryInstance that's the url to access it
    c.pop = 1000 # define the population
    c.gen = 1000 # define the generations
    
Or the other option is to use the GUI to generate an XML file or ofcourse generate it yourself. Try running
the GUI by starting UI.py. Try generating an XML file.
    


Advanced Example
=================================================================================================
Custom Primitives:
In more advance cases you would want to configure the framework ourselves. You might want to activate
special features or set certain parameters. For example primitive sets might not be good enough
and you need additional one. What you need to do is simply extend PrimitiveConfig.

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
                      "fitnessFunction","numberOfFunctionArgs","getFunctions","basicPrimitives"
                      ,"requestHandler","responseHandler", "handler",]
every other method name is generating a primitive for the framework to use.
Update the basic example to use primitive sets that you've created.

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


