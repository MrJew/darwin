__author__ = 'MrJew'

def listTokwags(dicOfLists):
    newArgs=[]
    for i in range(len(dicOfLists.values()[0])):
        nd={}
        for key in dicOfLists.keys():
            nd[key]=dicOfLists[key][i]
        newArgs.append(nd)
    print "IN",newArgs
    return newArgs