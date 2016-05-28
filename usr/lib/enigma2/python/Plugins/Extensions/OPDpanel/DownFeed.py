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

#####################################################################################
# DownFeed
####################################################################################
class InstallFeed(Screen):
	skin = """
		<screen name="InstallFeed" position="center,center" size="750,560" title="Insatall extensions from feed" >
		<widget name="a_off" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/aoff.png" position="10,10" zPosition="1" size="36,97" alphatest="on" />
			<widget name="a_red" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/ared.png" position="10,10" zPosition="1" size="36,97" alphatest="on" />
			<widget name="a_yellow" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/ayellow.png" position="10,10" zPosition="1" size="36,97" alphatest="on" />
			<widget name="a_green" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OPDpanel/icons/agreen.png" position="10,10" zPosition="1" size="36,97" alphatest="on" />
			<widget name="feedstatusRED" position="60,14" size="200,30" zPosition="1" font="Regular;25" halign="left" transparent="1" />
			<widget name="feedstatusYELLOW" position="60,46" size="200,30" zPosition="1" font="Regular;25" halign="left" transparent="1" />
			<widget name="feedstatusGREEN" position="60,78" size="200,30" zPosition="1" font="Regular;25" halign="left" transparent="1" />
			<widget name="packagetext" position="180,50" size="350,30" zPosition="1" font="Regular;25" halign="right" transparent="1" />
			<widget name="packagenr" position="511,50" size="50,30" zPosition="1" font="Regular;25" halign="right" transparent="1" />
			<widget source="list" render="Listbox" position="10,120" size="630,365" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (5, 1), size = (540, 28), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 0 is the name
							MultiContentEntryText(pos = (5, 26), size = (540, 20), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 2 is the description
							MultiContentEntryPixmapAlphaTest(pos = (545, 2), size = (48, 48), png = 4), # index 4 is the status pixmap
							MultiContentEntryPixmapAlphaTest(pos = (5, 50), size = (610, 2), png = 5), # index 4 is the div pixmap
						],
					"fonts": [gFont("Regular", 22),gFont("Regular", 14)],
					"itemHeight": 52
					}
				</convert>
			</widget>
			<ePixmap pixmap="skin_default/buttons/red.png" position=" 30,570" size="35,27" alphatest="blend" />
			<widget name="key_green_pic" pixmap="skin_default/buttons/green.png" position="290,570" size="35,27" alphatest="blend" />
			<widget name="key_red" position=" 80,573" size="200,26" zPosition="1" font="Regular;22" halign="left" transparent="1" />
			<widget name="key_green" position="340,573" size="200,26" zPosition="1" font="Regular;22" halign="left" transparent="1" />
		</screen> """
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.setup,
				"green": self.setup,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		
	def nList(self):
		self.list = []
		os.system("opkg update")
		try:
			ipklist = os.popen("opkg list")
		except:
			pass
		
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0] + dstring[1]+ dstring[2]+dstring[3]) + 4

				self.list.append((dstring[0]  + " " + dstring[1] + " " + dstring[2], line[endstr:]))
			except:
				pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def setup(self):
		item = self["menu"].getCurrent()
		name = item[0]
		os.system("opkg install -force-reinstall %s" % name)
		msg  = _("%s is installed" % name)
		self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout = 4 )



