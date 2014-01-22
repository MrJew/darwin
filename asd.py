__author__ = 'mrjew'

class Start:
    arg1 = None
    arg2 = 2
    arg3 = 4

    def start(self):
        locals()['arg1'] = 2
        print self.arg1

Start().start()