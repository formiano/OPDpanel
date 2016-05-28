from enigma import eTimer
from os import system, listdir, chdir, getcwd, remove as os_remove
import os
import urllib
from urllib2 import Request, urlopen, URLError, HTTPError
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from Screens.InputBox import InputBox, PinInput
from Screens.ChoiceBox import ChoiceBox
from enigma import eTimer, eConsoleAppContainer
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Components.Label import Label
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.FileList import FileList
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import PluginList
from Components.Button import Button
from Components.Input import Input
from Plugins.Plugin import PluginDescriptor
from ServiceReference import ServiceReference
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_SKIN_IMAGE, fileExists, pathExists, createDir, SCOPE_PLUGINS
from Tools import Notifications
from Tools.NumericalTextInput import NumericalTextInput
from Tools.LoadPixmap import LoadPixmap
from Tools.BoundFunction import boundFunction

class AddonsUtility(Screen):
    skin = '\n\t\t<screen name="AddonsUtility" position="center,60" size="800,635" title="OPD Addons Manager" >\n\t\t<widget name="list" position="80,100" size="510,350" zPosition="2" scrollbarMode="showOnDemand" transparent="1"/>\n\t\t<widget name="key_red" position="135,600" zPosition="1" size="180,45" font="Regular;20" foregroundColor="red" backgroundColor="red" transparent="1" />\t\t\n\t\t<widget name="key_green" position="410,600" zPosition="1" size="250,45" font="Regular;20" foregroundColor="green" backgroundColor="green" transparent="1" />\n\t\t<widget name="key_yellow" position="675,600" zPosition="1" size="180,45" font="Regular;20" foregroundColor="yellow" backgroundColor="yellow" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self.entrylist = []
        self.entrylist.append((_('Plugin'), 'Plg', '/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/Plugin.png'))
        self.entrylist.append((_('Picons'), 'Pcs', '/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/Picons.png'))
        self.entrylist.append((_('Setting'), 'Stg', '/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/Setting_list.png'))
        self.entrylist.append((_('Skin'), 'Sks', '/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/Skins.png'))
        self.entrylist.append((_('BootLogo'), 'Logo', '/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/BootLogo.png'))
        self['list'] = PluginList(self.list)
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Remove'))
        self['key_yellow'] = Label(_('Restart E2'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'back': self.close,
         'green': self.Remove,
         'yellow': self.RestartE2})
        self.onLayoutFinish.append(self.updateList)

    def Remove(self):
        self.session.open(AddonsRemove)

    def RestartE2(self):
        msg = 'Do you want Restart GUI now ?'
        self.session.openWithCallback(self.Finish, MessageBox, msg, MessageBox.TYPE_YESNO)

    def Finish(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def KeyOk(self):
        selection = self['list'].getCurrent()[0][1]
        print selection
        if selection == 'Plg':
            addons = 'Plugins'
            self.title = ' OPD Downloader Plugins'
            self.session.open(Connection_Server, addons, self.title)
        elif selection == 'Pcs':
            addons = 'Picons'
            self.title = ' OPD Downloader Picons'
            self.session.open(Connection_Server, addons, self.title)
        elif selection == 'Stg':
            addons = 'Setting'
            self.title = ' OPD Downloader Settings '
            self.session.open(Connection_Server, addons, self.title)
        elif selection == 'Sks':
            addons = 'Skins'
            self.title = 'OPD Downloader Skins '
            self.session.open(Connection_Server, addons, self.title)
        elif selection == 'Logo':
            addons = 'BootLogo'
            self.title = ' OPD Downloader BootLogo '
            self.session.open(Connection_Server, addons, self.title)
        else:
            self.messpopup('Selection error')

    def messpopup(self, msg):
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)

    def updateList(self):
        for i in self.entrylist:
            res = [i]
            res.append(MultiContentEntryText(pos=(60, 5), size=(300, 48), font=0, text=i[0]))
            picture = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, i[2]))
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(48, 48), png=picture))
            self.list.append(res)

        self['list'].l.setList(self.list)



class	AddonsRemove(Screen):
	
	skin = """
		<screen name="AddonsRemove" position="80,95" size="620,450" title="Addons Packages Remove">
		<widget source="list" render="Listbox" position="10,10" size="600,300" scrollbarMode="showOnDemand" >
		<convert type="StringList" />
		</widget>	
		<widget name="key_red" position="70,355" zPosition="1" size="200,60" font="Regular;20"  foregroundColor="red" backgroundColor="red" transparent="1" />		  
		<widget name="key_green" position="350,355" zPosition="1" size="200,60" font="Regular;20"  foregroundColor="green" backgroundColor="green" transparent="1" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label(_('Remove Addons'))
		self.list = []	
		self['list'] = List(self.list)
		self.container = eConsoleAppContainer()	
		self.container.appClosed.append(self.runFinished)
		self['actions'] = ActionMap(['WizardActions','ColorActions'],
		{
			'ok': self.KeyOk,
			"red": self.close,
			'green': self.KeyOk,
			'back': self.close
		})
		self.onLayoutFinish.append(self.ReadFile)
	def ReadFile(self):
		idx = 0
		pkgs = listdir('/usr/uninstall')
		for fil in pkgs:
			if (fil.find('.del') != -1 or fil.find('.sh') != -1):
				res = (fil, idx)
				self.list.append(res)
				idx = idx + 1
				continue
			
	def KeyOk(self):
		self.sel = self['list'].getCurrent()
		if self.sel:
			self.sel
			self.sel = self.sel[0]
			message = 'Do you want remove :\n'+ self.sel + ' ?'
			ybox = self.session.openWithCallback(self.removeAddons, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle('Removed Confirm')
		else:
			self.sel
	
	def removeAddons(self, answer):
		if (answer is True):
			self.container.execute("/usr/uninstall/" + self.sel)
			#self.container.execute("/usr/uninstall/%s" % self.sel)
	def runFinished(self, retval):
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		msg="Plugin %s uninstalled" % self.sel
    		self.session.open(MessageBox, msg , MessageBox.TYPE_INFO, timeout = 6)
		self.close()


class Connection_Server(Screen):
    skin = '\n\t\t<screen name="Connection_Server" position="center,center" size="650,500" title="OPD Download Manager">\n\t\t<widget name="list" position="10,10" size="600,400" scrollbarMode="showOnDemand" transparent="1" />\n\t\t<eLabel position="70,100" zPosition="-1" size="200,200" foregroundColor="white" />\n\t\t<widget name="info" position="100,300" zPosition="4" size="300,60" font="Regular;18" transparent="1" />\n\t\t</screen>'

    def __init__(self, session, addons, title):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = MenuList([])
        self['info'] = Label()
        self.mytitle = title
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.okClicked,
         'cancel': self.close}, -1)
        self.addon = addons
        self.icount = 0
        self.onLayoutFinish.append(self.Connection)

    def Connection(self):
        xurl = 'http://' + self.addon + '/list'
        xdest = '/tmp/ipklist.txt'
        print 'xdest =',
        print xdest
        try:
            xlist = urllib.urlretrieve(xurl, xdest)
            myfile = file('/tmp/ipklist.txt')
            self.data = []
            self.names = []
            icount = 0
            list = []
            for line in myfile.readlines():
                self.data.append(icount)
                self.names.append(icount)
                self.data[icount] = line[:-1]
                ipkname = self.data[icount]
                print 'icount, ipk name =',
                print icount,
                print ipkname
                remname = ipkname
                self.names[icount] = remname
                icount = icount + 1

            self['list'].setList(self.names)
        except:
            self['info'].setText('Server not found!\nPlease check internet connection.')

    def okClicked(self):
        sel = self['list'].getSelectionIndex()
        ipk = self.data[sel]
        addon = self.addon
        message = 'Do you want install :\n' + ipk + '?'
        ybox = self.session.openWithCallback(self.install, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle('Installation Confirm')

    def install(self, answer):
        if answer is True:
            sel = self['list'].getSelectionIndex()
            ipk = self.data[sel]
            addon = self.addon
            self.session.open(Installer_Addons, ipk, addon)
        else:
            self.close()


class Installer_Addons(Screen):
    skin = '\n\t\t<screen name="Installer_Addons" position="center,center" size="550,500" title="Installation Process" >\n\t\t<widget name="infotext" position="10,0" size="520,450" />\n\t\t<eLabel position="70,100" zPosition="-1" size="100,69" foregroundColor="white" />\n\t\t<widget name="info" position="100,300" zPosition="4" size="300,60" font="Regular;22" transparent="1" />\n\t\t</screen>'

    def __init__(self, session, ipk, addon):
        Screen.__init__(self, session)
        self['infotext'] = ScrollLabel('')
        self['info'] = Label()
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.close,
         'cancel': self.close}, -1)
        self.icount = 0
        self.ipk = ipk
        self.addon = addon
        self.onLayoutFinish.append(self.Install)

    def Install(self):
        xurl1 = 'http://' + self.addon + '/'
        xurl2 = xurl1 + self.ipk
        xdest2 = '/tmp/' + self.ipk
        print 'xdest2 =',
        print xdest2
        try:
            xlist = urllib.urlretrieve(xurl2, xdest2)
            self['info'].setText('')
            cmd = 'opkg install -force-overwrite /tmp/' + self.ipk + '>/tmp/ipk.log'
            os.system(cmd)
            self.viewLog()
        except:
            self['info'].setText('Installation failed!\nPlease check internet connection.')

    def viewLog(self):
        strview = ''
        print 'In viewLog'
        if os.path.isfile('/tmp/ipk.log') is not True:
            cmd = 'touch /tmp/ipk.log'
            os.system(cmd)
        else:
            myfile = file('/tmp/ipk.log')
            icount = 0
            data = []
            for line in myfile.readlines():
                data.append(icount)
                print line
                num = len(line)
                data[icount] = line[:-1]
                print data[icount]
                icount = icount + 1
                strview += line + '\n'

            self['infotext'].setText(strview)
            self.endinstall()

    def endinstall(self):
        path = '/tmp'
        tmplist = []
        ipkname = 0
        tmplist = os.listdir(path)
        print 'files in /tmp', tmplist
        icount = 0
        for name in tmplist:
            nipk = tmplist[icount]
            if nipk[-3:] == 'ipk':
                ipkname = nipk
            icount = icount + 1

        if ipkname != 0:
            print 'endinstall ipk name =', ipkname
            ipos = ipkname.find('_')
            remname = ipkname[:ipos]
            print 'endinstall remname =', remname
            f = open('/etc/ipklist_installed', 'a')
            f1 = remname + '\n'
            f.write(f1)
            cmd = 'rm /tmp/*.ipk'
            os.system(cmd)
