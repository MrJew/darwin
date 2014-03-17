__author__ = 'mrjew'
import wx
import wx.lib.agw.floatspin as fs
from primitiveConfig import PrimitiveConfig
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import sys
import csv
from xmlParser import *
from urlparse import urlparse,urlsplit

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)



class UI(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)

        self.InitUI()
        self.Center()
        self.Show()

    def InitUI(self):
        self.InitMenu()

        textPanel = self.InitTexts()
        attrPanel = self.InitAttributes()
        primPanel = self.InitPrimitives()
        buttPanel = self.InitButtons()

        panel = wx.Panel(self,-1)
        sizer = wx.GridBagSizer(2,2)
        sizer.Add(textPanel,pos=(1,1))
        sizer.Add(primPanel,pos=(1,2))
        sizer.Add(attrPanel,pos=(2,1))
        sizer.Add(buttPanel,pos=(2,2))

        panel.SetSizer(sizer)



        self.SetSize((800, 400))
        self.SetTitle('Darwin')
        self.Centre()
        self.Show(True)

    def InitMenu(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        menubar.Append(fileMenu, '&File')

        self.SetMenuBar(menubar)

    def InitTexts(self):
        panel = wx.Panel(self,-1)
        sizer = wx.GridBagSizer(4,2)

        #filetxt = wx.StaticText(panel, label="File Name")
        #sizer.Add(filetxt,pos=(0,0), flag = wx.LEFT|wx.TOP)
        #self.file = wx.TextCtrl(panel,style=wx.TE_LEFT)
        #sizer.Add(self.file, span=(1,20), pos=(1,0), flag = wx.TOP|wx.EXPAND|wx.BOTTOM)

        clienttxt = wx.StaticText(panel, label="Client IP Adress")
        sizer.Add(clienttxt,pos=(0,0), flag = wx.LEFT|wx.TOP)
        self.client = wx.TextCtrl(panel,style=wx.TE_LEFT)
        sizer.Add(self.client, span=(1,20), pos=(1,0), flag = wx.TOP|wx.EXPAND|wx.BOTTOM)

        portclientxt = wx.StaticText(panel, label="Port")
        sizer.Add(portclientxt,pos=(0,21), flag = wx.LEFT|wx.TOP)
        self.portclient = wx.TextCtrl(panel,style=wx.TE_LEFT)
        sizer.Add(self.portclient, pos=(1,21), flag = wx.TOP|wx.EXPAND|wx.BOTTOM)

        tartgettxt = wx.StaticText(panel, label="Target IP Adress")
        sizer.Add(tartgettxt,pos=(2,0), flag = wx.LEFT|wx.TOP|wx.EXPAND)
        self.target = wx.TextCtrl(panel,style=wx.TE_LEFT)
        sizer.Add(self.target, span=(1,20),pos=(3,0), flag = wx.TOP|wx.EXPAND|wx.BOTTOM)

        porttargetxt = wx.StaticText(panel, label="Port")
        sizer.Add(porttargetxt,pos=(2,21), flag = wx.LEFT|wx.TOP)
        self.porttarget = wx.TextCtrl(panel,style=wx.TE_LEFT)
        sizer.Add(self.porttarget, pos=(3,21), flag = wx.TOP|wx.EXPAND|wx.BOTTOM)

        panel.SetSizer(sizer)
        return panel

    def InitAttributes(self):

        panel = wx.Panel(self,-1)

        sizer = wx.GridBagSizer(5, 5)

        #### Column 1

        poptxt = wx.StaticText(panel, label="Population")
        sizer.Add(poptxt, pos=(0, 0), flag=wx.LEFT|wx.TOP, border=20)

        self.pop = wx.SpinCtrl(panel,value='1000',min=1,max=10000)
        sizer.Add(self.pop, pos=(0, 1), flag=wx.TOP,border=15)

        ####
        gentxt = wx.StaticText(panel, label="Generation")
        sizer.Add(gentxt, pos=(1, 0), flag=wx.LEFT|wx.TOP, border=20)

        self.gen = wx.SpinCtrl(panel,value='1000',min=1,max=10000)
        sizer.Add(self.gen, pos=(1, 1),  flag=wx.TOP, border=15)
        ####
        muttxt = wx.StaticText(panel, label="Mutation")
        sizer.Add(muttxt, pos=(2, 0), flag=wx.TOP|wx.LEFT, border=20)

        self.mut = fs.FloatSpin(panel,value='0.2',digits=1,increment=0.1)
        self.mut.SetRange(0.0,1.0)
        sizer.Add(self.mut,pos=(2,1), flag=wx.TOP, border=15,)

        ####
        cxtxt = wx.StaticText(panel, label="Crossing")
        sizer.Add(cxtxt, pos=(3, 0), flag=wx.TOP|wx.LEFT, border=20)

        self.cx = fs.FloatSpin(panel,value='0.8',digits=1,increment=0.1)
        self.cx.SetRange(0.0,1.0)
        self.cx.SetSize((100,40))
        sizer.Add(self.cx,pos=(3,1), flag=wx.TOP, border=15)
        #### Column 2

        arg = wx.StaticText(panel, label="Test Arguments")
        sizer.Add(arg, pos=(0, 4), flag=wx.LEFT|wx.TOP, border=20)

        self.argtxt = wx.TextCtrl(panel)
        sizer.Add(self.argtxt, pos=(1, 4), span=(1,3), flag=wx.LEFT|wx.TOP|wx.EXPAND, border=10)

        argbutton = wx.Button(panel, label="Browse...",size=(80,20))
        sizer.Add(argbutton, pos=(0, 5), flag=wx.TOP,border=15)
        self.Bind(wx.EVT_BUTTON, self.OnBrowse, id=argbutton.GetId())

        ###
        ter = wx.StaticText(panel, label="Terminals")
        sizer.Add(ter, pos=(2, 4), flag=wx.LEFT|wx.TOP, border=20)

        self.tertxt = wx.TextCtrl(panel)
        sizer.Add(self.tertxt, pos=(3, 4), span=(1,3),  flag=wx.LEFT|wx.TOP|wx.EXPAND, border=10)



        #wx.SpinCtrl(pnl, value='1', pos=(55, 90), size=(60, -1), min=1, max=120)
        sizer.AddGrowableCol(4)

        panel.SetSizer(sizer)
        return panel


    def InitPrimitives(self):

        panel = wx.Panel(self,-1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)

        self.list = CheckListCtrl(rightPanel)
        self.list.InsertColumn(0, 'Primitive', width=150)

        primitives = PrimitiveConfig().basicPrimitives

        for i in primitives:
            self.list.InsertStringItem(sys.maxint, i)

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        sel = wx.Button(leftPanel, -1, 'Select All', size=(100, -1))
        des = wx.Button(leftPanel, -1, 'Deselect All', size=(100, -1))


        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())

        vbox2.Add(sel, 0, wx.TOP, 5)
        vbox2.Add(des)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)

        rightPanel.SetSizer(vbox)

        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)
        return panel

    def InitButtons(self):

        panel = wx.Panel(self,-1)

        sizer = wx.GridBagSizer(5, 5)


        genb = wx.Button(panel,-1,'Generate',size=(100,-1))
        sizer.Add(genb,border=25, pos=(5,5),flag=wx.TOP|wx.LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnGenerate, id=genb.GetId())

        panel.SetSizer(sizer)

        return panel

    # Event Handlers

    def OnQuit(self,e):
        self.Close()

    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)

    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)

    def OnBrowse(self,event):
        openFileDialog = wx.FileDialog(self,"Open .csv arguments file","","",
                                       "CSV files (*.csv)|*.csv",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.argtxt.SetValue(str(openFileDialog.GetPath()))

    def OnGenerate(self,event):

        saveFileDialog = wx.FileDialog(self, "Save XML file", "", "",
                                   "XML files (*.xml)|*.xml", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # save the current contents in the file
        # this can be done with e.g. wxPython output streams:

        parameters = {}
        if self.client.GetValue() == "" :
            wx.MessageBox('Client IP adress is required!', 'Error', wx.OK | wx.ICON_ERROR)
            return

        cport = self.portclient.GetValue()
        curl = self.client.GetValue()
        tport = self.porttarget.GetValue()
        turl = self.target.GetValue()

        o = urlparse(curl)
        curl = o.scheme+"://"+o.netloc
        if cport!="":
            curl+=":"+cport
        curl+=o.path

        o = urlparse(turl)
        turl = o.scheme+"://"+o.netloc
        if tport!="":
            turl+=":"+tport
        turl+=o.path

        parameters["evalUrl"]   = curl
        if self.target.GetValue() != "" : parameters["copyUrl"]   = turl
        if self.pop.GetValue() != "" : parameters["pop"]       = str(self.pop.GetValue())
        if self.gen.GetValue() != "" : parameters["gen"]       = str(self.gen.GetValue())
        if self.mut.GetValue() != "" : parameters["mut"]       = str(self.mut.GetValue())
        if self.cx.GetValue() != "" : parameters["cx"]        = str(self.cx.GetValue())
        parameters["fname"]     = str(saveFileDialog.GetPath())



        ### terminals ###
        if self.tertxt.GetValue() != "":
            terminals = self.tertxt.GetValue().split(",")
            for t in range(len(terminals)):
                terminals[t] = float(terminals[t])
            parameters["terminals"] = terminals

        #### primitives ####
        num = self.list.GetItemCount()
        primitives=[]
        for i in range(num):
            if self.list.IsChecked(i):
                primitives.append(str(self.list.GetItemText(i)))
        parameters["primitives"]= primitives

        #### args ####
        if self.argtxt.GetValue() != "":
            args={}
            f = open(self.argtxt.GetValue(),"rb")
            reader = csv.reader(f)
            for row in reader:
                key = row.pop(0)
                args[key]=row
            f.close()
            parameters["arguments"] = args

        generateXML(**parameters)
        self.success(parameters["fname"])

    def success(self,fname):
        wx.MessageBox('XML configuration file:'+ fname +' generated  !', 'Generation Successful', wx.OK | wx.ICON_INFORMATION)
        return


def main():

    ex = wx.App()
    UI(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()