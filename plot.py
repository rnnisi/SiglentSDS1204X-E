#!/usr/bin/env python3
#

import matplotlib.pyplot as plt
import numpy
import sys

args = sys.argv

exp = args[1]

df = 'ScreenDump_' + str(exp) + '.csv'

dat = open(df, 'r')
raw = str(dat.read())
lines = list(raw.split('\n'))
time = []
volts = []
for i in range(1, len(lines)):
	try:
		temp = str(lines[i]).split(', ')
		print(temp)
		volts.append(float(temp[1]))
		time.append(float(temp[0]))
	except:
		pass
title = str(lines[0]).split(', ')

plt.plot(time, volts)
plt.xlabel(title[0])
plt.ylabel(title[1])
plt.title(str(df))
plt.show()

input("press Enter to escape")
