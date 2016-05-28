from enigma import eTimer, eConsoleAppContainer
from Screens.InputBox import InputBox
from Screens.Setup import Setup
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap,NumberActionMap
from Components.ScrollLabel import *
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.PluginComponent import plugins
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, NoSave, configfile
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN
from os import system, remove as os_remove, rename as os_rename, popen, getcwd, chdir, statvfs, listdir
from os import rename, remove, stat as mystat
from Plugins.Plugin import PluginDescriptor
#import time
#import datetime
import Screens.MessageBox
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.PluginList import PluginList
from Screens.ChoiceBox import ChoiceBox
import stat, os, time ,datetime
from Components.Button import Button
from Components.Sources.StaticText import StaticText
mypanel = None

###########################
# Manual Pannel installer #
###########################

class ManualPanel(Screen):
	skin = """<screen name=" ManualPanel" position="80,100" size="560,410" title="Pannel installer">
		  <widget source="list" render="Listbox" position="10,10" size="540,300" scrollbarMode="showOnDemand" >
		  <convert type="StringList" />
		  </widget>
		  <widget name="key_green" position="225,355" zPosition="1" size="140,40" font="Regular;20" foregroundColor="green" backgroundColor="green" transparent="1" />
		  </screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.list=[]
		self.entrylist = []  #List reset
		self.entrylist.append((_("TarGz packages installer"), "one", "/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/File_Archive.png"))
		self.entrylist.append((_("Ipk packages installer"), "two", "/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/File_Archive.png"))
                self.entrylist.append((_("Advanced ipk packages installer"), "tree", "/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/File_Archive.png"))	
		self.entrylist.append((_("Ipk remove"), "four", "/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/File_Archive.png"))	
		self['list'] = PluginList(self.list)
		self['actions'] = ActionMap(['WizardActions','ColorActions'],
		{"ok": self.OK,
		 "back": self.exit,
		})
		self.onLayoutFinish.append(self.updateList)
	def exit(self):
		self.close()
	def OK(self):
		selection = self["list"].getCurrent()[0][1]
		if (selection == "one"):
			self.session.open(PanelTGzInstaller)
		elif (selection== "two"):
			self.session.open(PanelIPKInstaller)
		elif (selection== "tree"):
			self.session.open(AdvInstallIpk)
		elif (selection== "four"):
			self.session.open(RemoveIPK)
		else:
			self.messpopup("Selection error")
			
	def messpopup(self,msg):
		self.session.open(MessageBox, msg , MessageBox.TYPE_INFO)

	def updateList(self):
		for i in self.entrylist:
				res = [i]
				res.append(MultiContentEntryText(pos=(50, 5), size=(300, 32), font=0, text=i[0]))
				picture=LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, i[2]))
				res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(34, 34), png=picture))
				self.list.append(res)
		self['list'].l.setList(self.list)	

#################
# Ipk Installer #
#################
class PanelIPKInstaller(Screen):
	skin = """
    		<screen name="InstallIpk" position="center,100" size="750,520" title="Select ipk Files">
		<widget source="list" render="Listbox" position="10,10" size="880,300" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
		{"template": [
		MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 50), png = 2), # index 4 is the pixmap
		],
		"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
		"itemHeight": 60
		}
		</convert>
		</widget>
		<ePixmap position="15,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/redpanel.png" transparent="1" alphatest="on" />
		<ePixmap position="180,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/greenpanel.png" transparent="1" alphatest="on" />
		<widget source = "key_red" render="Label" position="29,385" zPosition="2" size="120,26" valign="center" halign="center" font="Regular;22" transparent="1" />
		<widget source = "key_green" render="Label" position="224,385" zPosition="2" size="350,26" valign="center" halign="left" font="Regular;22" transparent="1" />
        <eLabel position="10,375" size="880,2" backgroundColor="blue" foregroundColor="bluette" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label(_('Install ipk'))
		self.flist = []
		idx = 0
		pkgs = listdir('/tmp')
		for fil in pkgs:
			if fil.find('.ipk') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
				continue
		self['list'] = List(self.flist)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], 
		{'ok': self.KeyOk, 
		 'red':self.close, 
		 'green':self.KeyOk, 
		 'back': self.close})

	def KeyOk(self):
		self.sel = self['list'].getCurrent()
		if self.sel:
			self.sel
			self.sel = self.sel[0]
			message = 'Do you want to install the Addon:\n ' + self.sel + ' ?'
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle('Installation Confirm')
		else:
			self.sel

	def installadd2(self, answer):
		if answer is True:
			dest = '/tmp/' + self.sel
			mydir = getcwd()
			chdir('/')
			cmd = 'opkg install -force-overwrite ' + dest
			cmd2 = 'rm -f ' + dest
			self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd, cmd2])
			chdir(mydir)
			
#####################################################################################################
# Tar.Gz Installer
####################################################################################################
class PanelTGzInstaller(Screen):
	skin = """
    		<screen name="InstallTarGZ" position="center,100" size="750,520" title="Select tar.gz , bh.tgz , nab.tgz Files">
		<widget source="list" render="Listbox" position="10,10" size="880,300" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
		{"template": [
		MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 50), png = 2), # index 4 is the pixmap
		],
		"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
		"itemHeight": 60
		}
		</convert>
		</widget>
		<ePixmap position="15,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/redpanel.png" transparent="1" alphatest="on" />
		<ePixmap position="180,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/greenpanel.png" transparent="1" alphatest="on" />
		<widget source = "key_red" render="Label" position="29,385" zPosition="2" size="120,26" valign="center" halign="center" font="Regular;22" transparent="1" />
		<widget source = "key_green" render="Label" position="224,385" zPosition="2" size="350,26" valign="center" halign="left" font="Regular;22" transparent="1" />
        <eLabel position="10,375" size="880,2" backgroundColor="blue" foregroundColor="bluette" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label(_('Install Tgz'))
		self.flist = []
		idx = 0
		pkgs = listdir('/tmp')
		for fil in pkgs:
			if fil.find('.tgz') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
				continue
		self['list'] = List(self.flist)
		self['actions'] = ActionMap(['WizardActions', 'ColorActions'], 
		{'ok': self.KeyOk, 
		 'red':self.close,
		 'green':self.KeyOk,  
		 'back': self.close})

	def KeyOk(self):
		self.sel = self['list'].getCurrent()
		if self.sel:
			self.sel
			self.sel = self.sel[0]
			message = 'Do you want to install the Addon:\n ' + self.sel + ' ?'
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle('Installation Confirm')
		else:
			self.sel

	def installadd2(self, answer):
		if answer is True:
			dest = '/tmp/' + self.sel
			mydir = getcwd()
			chdir('/')
			cmd = 'tar -C/ -xzpvf ' + dest
			cmd2 = 'rm -f ' + dest
			self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd, cmd2])
			chdir(mydir)
			
				

	def Restart(self, answer):
		rc = system('killall -9 enigma2')



######################################################################################################
# Advance ipk Installer
######################################################################################################
class AdvInstallIpk(Screen):
	skin = """
    		<screen name="AdvInstallIpk" position="center,100" size="750,520" title="Advance ipk Installer">
		<widget source="menu" render="Listbox" position="10,10" size="880,300" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
		{"template": [
		MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 50), png = 2), # index 4 is the pixmap
		],
		"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
		"itemHeight": 60
		}
		</convert>
		</widget>
		<ePixmap position="15,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/redpanel.png" transparent="1" alphatest="on" />
		<ePixmap position="180,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/greenpanel.png" transparent="1" alphatest="on" />
                            <ePixmap position="350,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/yellowpanel.png" transparent="1" alphatest="on" />
		<widget source = "key_red" render="Label" position="43,385" zPosition="2" size="120,26" valign="center" halign="center" font="Regular;22" transparent="1" />
		<widget source = "key_green" render="Label" position="224,385" zPosition="2" size="350,26" valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget source = "key_yellow" render="Label" position="392,385" zPosition="2" size="350,26" valign="center" halign="left" font="Regular;22" transparent="1" />
        <eLabel position="10,375" size="880,2" backgroundColor="blue" foregroundColor="bluette" />
		</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.okInstAll,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.ipk")
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0]))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = _("Install ipk packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % name])
		except:
			pass
		
	def okInstAll(self):
		name = "*.ipk"
		self.session.open(Console,title = _("Install ipk packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % name])
		
	def cancel(self):
		self.close()
######################################################################################################
# Ipk Remove
######################################################################################################
class RemoveIPK(Screen):
	skin = """
    		<screen name="RemoveIPK" position="center,100" size="750,520" title="Remove-IPK">
		<widget source="menu" render="Listbox" position="10,10" size="880,300" scrollbarMode="showOnDemand">

		<convert type="TemplatedMultiContent">
		{"template": [
		MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 50), png = 2), # index 4 is the pixmap
		],

		"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
		"itemHeight": 60
		}
		</convert>
		</widget>
		<ePixmap position="10,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/redpanel.png" transparent="1" alphatest="on" />
		<ePixmap position="180,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/greenpanel.png" transparent="1" alphatest="on" />
                            <ePixmap position="350,385" zPosition="1" size="35,27" pixmap="/usr/share/enigma2/oDreamy/buttons/yellowpanel.png" transparent="1" alphatest="on" />
		<widget source = "key_red" render="Label" position="36,385" zPosition="2" size="120,26" valign="center" halign="center" font="Regular;22" transparent="1" />
		<widget source = "key_green" render="Label" position="220,385" zPosition="2" size="350,26" valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget source = "key_yellow" render="Label" position="390,385" zPosition="2" size="350,26" valign="center" halign="left" font="Regular;22" transparent="1" />
        <eLabel position="10,375" size="880,2" backgroundColor="blue" foregroundColor="bluette" />
		</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnInstall"))
		self["key_yellow"] = StaticText(_("Force UnInstall"))
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.Remove,
				"green": self.Remove,
				"red": self.cancel,
				"yellow": self.ARemove,
			},-1)
		
	def nList(self):
		self.list = []
		ipklist = os.popen("opkg list-installed")
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0]) + 2
				self.list.append((dstring[0], line[endstr:]))
			except:
				pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def Remove(self):
		item = self["menu"].getCurrent()
		name = item[0]
		os.system("opkg remove %s" % item[0])
		self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % item[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()

	def ARemove(self):
		item = self["menu"].getCurrent()
		os.system("opkg remove -force-remove %s" % item[0])
		self.mbox = self.session.open(MessageBox,_("%s is UnInstalled" % item[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()

