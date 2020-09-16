#!/usr/bin/env python3
# Rebecca Nishide, 9/3/2020
#

import SDS1204XE as sig
import time
import sys
import subprocess
import ExtractWfm
#port = 5025

""" 
Establish connection with scope 
"""

# set up 
sig = sig.SDS1204XE()
sig.checkargs(3)
out, exp = sig.ConfigOutput()
IP, rt = sig.getArgs()	# assign IP as given arguement 
dir = sig.mkdir()	# make a directory for results
sig.GoToInstrWebPage(IP)	
sig.FindAllButtons()
sig.OpenSidePanel()
sig.SocketCmd(b'TRMD AUTO')
sig.SocketCmd(b'C1:TRLV 1.5V')
sig.SocketClose()
xdiv, x_units = sig.TimeDivs()
ydiv, y_units = sig.VoltDivs()
print("time div: ", xdiv, x_units, "volt div:", ydiv, y_units)
st = sig.StartLog(dir, xdiv, ydiv)
i = 0	# count total trigger checks 
n = 0	# count number of waveforms collected
dat = open(out, 'w+')

# check and reset trigger 
while time.perf_counter() - float(st) < float(rt):
	i = i + 1
	sig.PressSingle()
	time.sleep(0.3)
	try:
		stat = sig.CheckTriggerButton()
		if stat == 'STOP':
			sig.ScreenGrab(i)
			n = n + 1
			print("getting waveform")
			dat.write("TRIGGERED, i = " + str(i) + ", time = " + str(time.perf_counter() - st) + '\n')
			time.sleep(0.5)
		else:
			print(stat)
			dat.write("i = "+ str(i) + ", time = " + str(time.perf_counter() - st) + '\n')
			time.sleep(0.1)
			pass
	except KeyboardInterrupt:
		break

sig.QuitDriver()
sig.EndLog(st, n, i)

"""
Extract waveform from csv
"""
# configure
path = './' + str(dir) 
ls = subprocess.check_output(['ls ' + path], shell = True)
ScreenShots = ls.split(b'\n')

# run extraction on each png to collect csv
for i in ScreenShots[:len(ScreenShots) -1]:
	print('i: ', i)
	fn = path + '/' + str(i)[2:len(i) -1]
	print('path: ', fn)
	png = ExtractWfm.open_png(fn + 'png')
	t, v = ExtractWfm.get_wfm(png)
	time, volts = ExtractWfm.cleanup(png, t, v)
	print(time, volts)
	x, y = ExtractWfm.GetDat(float(xdiv), float(ydiv), time, volts)
	csv = open(fn + 'csv', 'w+')
	csv.write('Time (' + x_units + '), Voltage (' + y_units + ')\n')
	for k, j in zip(x, y):
		csv.write(str(k) + ', ' + str(j)+ '\n')
	csv.close()
