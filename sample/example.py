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
        main = "http://api.wolframalpha.com/v2/query?appid="+apid+"&input=pi*("+str(params['r'])+"%5E2)&format=plaintext"
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
        print result
        return float(result)


configClass = Config()
c = Configuration(configClass=configClass,configXml="config.xml")
c.configure()
p = Populator(configuration=c)
p.populate()