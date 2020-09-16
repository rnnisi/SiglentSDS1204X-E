import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import socket
import os
import subprocess

class SDS1204XE:
	def __init__(self):
		#options = Options()
		#self.driver = webdriver.Chrome(options = options)
		self.LogF = "LOG.txt"
		self.f = "Exp_1.txt"
		self.ff = "'Exp_' + str(i) + '.txt'"
		#self.options = options
		#self.options.page_load_strategy = 'normal'
		self.port = 5025
	def ReadFile(self, infile):
		read = open(infile, 'r')
		lines = read.readlines()
		read.close()
		return(lines)
	def checkargs(self, NARGS):
		self.args = list(sys.argv)
		if len(self.args) != int(NARGS):
			print("Incorrect numbe of arguements given. Exiting...")
			sys.exit(0)
		else:
			pass
		return self.args
	def getArgs(self):
		self.IP = self.args[1]
		self.rt = self.args[2]
		return self.IP, self.rt
	def checkdir(self,f,ff):       # check names of files with name f, number output files to avoid overwriting
		i = 2				# format for f should be : NAME_n.txt with n = 1, 2, 3.....
		if os.path.exists(f) == False:
			out = open(f, 'w+')
		else:
			while os.path.isfile(f) == True:
				f = eval(ff)
				i = i+1
				os.path.isfile(f)
		return [str(f), str(i - 1)]	# output file will be returned as a string with name, number, and extension
	def ConfigOutput(self):
		config = self.checkdir(self.f, self.ff)
		self.out = config[0]
		self.exp = config[1]
		return config
	def mkdir(self):
		options = webdriver.ChromeOptions()
		options.page_load_strategy = 'normal'
		cmd = 'mkdir Exp_' + str(self.exp)
		dirct = "Exp_" + str(self.exp)
		subprocess.Popen([cmd], shell = True)
		self.wd = str(subprocess.check_output(['pwd'], shell = True))
		self.wd = self.wd[2:len(self.wd)-3]
		path =	self.wd + '/' + dirct
		SaveTo = eval(r'path')
		print(str(SaveTo))
		prefs = {"download.default_directory": path}
		options.add_experimental_option("prefs", prefs)
		self.driver = webdriver.Chrome(options = options)
		self.driver.set_window_size(1500, 1080)
		self.dirct = dirct
		return dirct
	def StartLog(self, dir, xdiv, ydiv):
		log = open('LOG.txt', 'a+')
		log.write('\n' + dir + ":  DateTime = " + str(time.asctime()) + ', TimeDiv = ' + str(xdiv) + ', VoltDiv = ' + str(ydiv) + ', ')
		st = time.perf_counter()
		log.close()
		return st
	def EndLog(self, st, n, i):
		RunTime = time.perf_counter() - st
		log = open('LOG.txt', 'a+')
		log.write('RunTime = ' + str(RunTime) + ', WfmCollected = ' + str(n) + ', Checks = ' + str(i) + '\n')
		log.close()
	def SocketConnect(self, IP, port):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print("Failed to create socket")
			sys.exit()
		self.s.connect((IP, port))
		self.s.setblocking(0)
		self.IP = IP
		self.port = port
		return self.s
	def SocketClose(self):
		self.s.close()
		time.sleep(0.3)
	def SocketQuery(self,cmd):
		try:
		#	self.SocketConnect(self.IP, self.host)
			self.s.sendall(cmd)
			self.s.sendall(b'\n')
			time.sleep(1)
		except socket.error:
			print("send failed")
			sys.exit(0)
		except ConnectionResetError:
			print("connection Reset error. trying to reconnect")
			self.SocketConnect(self.IP, self.port)
		#try:
		reply = self.s.recv(4096)
		self.SocketClose()
		return reply
		#except BlockingIOError:
		#	print("Data receive complete")
		#self.SocketClose()
	def SocketCmd(self, cmd):
		try:
			self.SocketConnect(self.IP, self.port)
			self.s.sendall(cmd)
			self.s.sendall(b'\n')
			time.sleep(0.5)
		except socket.error:
			print("Command failed to reach scope. Exiting...")
			sys.exit(0)
		except ConnectionResetError:
			self.SocketConnect(self.IP, self.port)
		self.SocketClose()
	def TrigStat(self):
		try:
			self.SocketConnect(self.IP, self.port)
			time.sleep(0.25)
			self.s.sendall(b'SAST?')
			self.s.sendall(b'\n')
			time.sleep(1)
		except socket.error:
			print("Cannot get trigger status")
		try:
			reply = self.s.recv(10)
			return reply
		except BlockingIOError:
			print("No response to trigger status query")
		self.SocketClose()
	def TimeDivs(self):
		try:
			self.SocketConnect(self.IP, self.port)
		except socket.error:
			print("Cannot get trigger status")
		try:
			time.sleep(0.25)
			self.s.sendall(b'TDIV?')
			self.s.sendall(b'\n')
			time.sleep(1)
			self.xdiv = self.s.recv(40)
		except BlockingIOError:
			print("No response to time div query")
			return '', ''
		self.SocketClose()
		self.xdiv = str(list(self.xdiv.split())[1])
		if self.xdiv.find('NS') != -1:
			units = 'ns'
		if self.xdiv.find('US') != -1:
			units = 'us'
		if self.xdiv.find('MS') != -1:
			units = 'ms'
		if self.xdiv.find('S') != -1:
			units = 's'
		self.xdiv = self.xdiv[2:len(self.xdiv) - len(units)-1]	
		return self.xdiv, units
	def VoltDivs(self):
		try:
			self.SocketConnect(self.IP, self.port)
		except socket.error:
			print("Cannot get trigger status")
		try:
			time.sleep(0.25)
			self.s.sendall(b'C1:VDIV?')
			self.s.sendall(b'\n')
			time.sleep(1)
			self.ydiv = self.s.recv(40)
		except BlockingIOError:
			print("No response to volt div query")
			return '', ''
		self.SocketClose()
		self.ydiv = str(list(self.ydiv.split())[1])
		units = ''
		if self.ydiv.find('V') != -1:
			units = 'V'
		if self.ydiv.find('mV') != -1:
			units = 'mV'
		if self.ydiv.find('uV') != -1:
			units = 'uV'
		if units == '':
			units = 'V'
		self.ydiv = self.ydiv[2:len(self.ydiv) - len(units) -1]
		return self.ydiv, units
	def GoToInstrWebPage(self,IP):
		self.url = "http://" + IP + "/Instrument/novnc/vnc_auto.php"
		self.driver.get(self.url)
		time.sleep(1)
	def Button_WfmBin(self):
		self.WfmBin = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[3]/div/button[2]')
	def Button_RunStop(self):
		self.RunStop = self.driver.find_element_by_id("Run_Stop")
	def Button_SidePanel(self):
		self.SidePanel = self.driver.find_element_by_id("panel_control")
	def Button_Single(self):
		self.Single = self.driver.find_element_by_id("Single")
	def Button_ScreenSave(self):
		self.ScreenSave = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[3]/div/button[1]')
	def OpenSidePanel(self):
		self.SidePanel.click()
		time.sleep(0.1)
	def FindAllButtons(self):
		self.Button_WfmBin()
		self.Button_SidePanel()
		self.Button_Single()
		self.Button_RunStop()
		self.Button_ScreenSave()
	def PressSingle(self):
		self.Single.click()
	def CheckTriggerButton(self):
		color = 'self.RunStop.value_of_css_property("background-color")'
		if eval(color) == 'rgba(255, 0, 0, 1)':
			self.trig = 'STOP'
		else:
			self.trig = 'RUN'
		return self.trig
	def GetBinWf(self):
		try:
			self.WfmBin.click()
		except:
			try:
				self.SidePanel.click()
				self.WfmBin.click()
			except:
				print("Unable to get binary waveform. Check:\n	  Connection to local host\n	Chrome window is big enough to avoid interference on waveform save button\n    Scope is responsive")
	def ScreenGrab(self, i):
		self.driver.save_screenshot("./" + self.dirct +"/ScreenDump_" + str(i) + ".png")
	def GetBMP(self):
		self.ScreenSave.click()
	def QuitDriver(self):
		self.driver.quit()

