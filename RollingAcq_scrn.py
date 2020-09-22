#!/usr/bin/env python3
# Rebecca Nishide, 9/3/2020
#

import SDS1204XE as sig
import time
import sys
import subprocess
import ExtractWfm
#port = 5025

# set up scope
sig = sig.SDS1204XE()
sig.checkargs(4) # check that right number of arguements are given 
out, exp = sig.ConfigOutput()
IP, rt, trig = sig.getArgs()
dir = sig.mkdir()	# make a directory for results
sig.GoToInstrWebPage(IP)	# open driver to scope online interface
sig.FindAllButtons()	# identify the buttons we will need
sig.OpenSidePanel()	# open side panel that has all the options
sig.SocketCmd(b'TRMD AUTO')	# set to auto over sicket
sig.SetTrig()	# set trigger level
sig.SocketClose()
xdiv, x_units = sig.TimeDivs()
ydiv, y_units = sig.VoltDivs()
print("\nTalking to scope...\n")
try:
	xdiv = float(xdiv)
	ydiv = float(ydiv)
except ValueError:
	print("Unable to get time and/or volt divs over LAN. Check configurations and try again. Exiting program...")
	sys.exit(0)

print("time div: ", xdiv, x_units, "volt div:", ydiv, y_units)
print("\nInitializing experiment...\n")
st = sig.StartLog(dir, xdiv, ydiv)
i, n = sig.Collect(st, rt, out)
sig.QuitDriver()
sig.EndLog(st, n, i)
print("\nConcluding DAQ...")
path = './' + str(dir) 
ls = subprocess.check_output(['ls ' + path], shell = True)
ScreenShots = ls.split(b'\n')
print("\nGenerating CSV's...\n")
for i in ScreenShots[:len(ScreenShots) -1]:
	fn = path + '/' + str(i)[2:len(i) -1]
	png = ExtractWfm.open_png(fn + 'png')
	t, v = ExtractWfm.get_wfm(png)
	time, volts = ExtractWfm.cleanup(png, t, v)
	x, y = ExtractWfm.GetDat(float(xdiv), float(ydiv), time, volts)
	csv = open(fn + 'csv', 'w+')
	csv.write('Time (' + x_units + '), Voltage (' + y_units + ')\n')
	for k, j in zip(x, y):
		csv.write(str(k) + ', ' + str(j)+ '\n')
	csv.close()
	print("CSV " + fn + "written.\n")
