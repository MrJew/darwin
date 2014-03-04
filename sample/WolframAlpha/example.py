__author__ = 'mrjew'
from configuration import *
from populator import *
from lxml import etree
from StringIO import StringIO

#apid= X63LWT-U7E9YX8R2K
class Config(PrimitiveConfig):

    def requestHandler(self,url,params):
        print params
        apid= "X63LWT-U7E9YX8R2K"
        formatw = "plaintext"
        expression="pi*("+str(params['r'])+"%5E2)"
        arguments = {'format':formatw,'input':expression,'appid':apid}
        #main = "?appid="+apid+"&input=pi*("+str(params['r'])+"%5E2)&format=plaintext"
        return self.handler(url,params=arguments)

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
        print result
        return float(result)


configClass = Config()
c = Configuration(configClass=configClass,configXml="wolframalpha.xml")
c.configure()
p = Populator(configuration=c)
p.populate()
p.generateWebService(p.hof[0])
print p.hof