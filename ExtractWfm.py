import sys
import PIL
import numpy as np
from PIL import Image


def open_png(path):
	img = Image.open(path)
	img = img.convert("RGB")
	#img = img.load()
	#img.show()
	#input("Press <Enter> to continue...")
	return img

def get_pixel(img, i, j):
	X, Y = img.size
	if i > X or j > Y:
		return None
	pixel = img.getpixel((i, j))
	if pixel[0] ==241:
		pass 
		#if pixel[0] < 246:
		#	pass		
	else:
		return False
	if pixel[1] >= 243:
		if pixel[1] < 247:
			pass
	else:
		return False
	if pixel[1] >= pixel[2]:
		pass
	else:
		return False
	if pixel[2] < 1 :
		if pixel[2] >= 0:
			return True
	else:
		return False
def get_black(img, i, j):
	X, Y = img.size
	if i > X or j > Y:
		return None
	pixel = img.getpixel((i, j))
	if pixel[1] == 0:
		pass
	else:
		return False
	if pixel[1] == 0:
		pass
	else:
		return False
	if pixel[1] >= pixel[2]:
		pass
	else:
		return False
	if pixel[2] == 0:
		return True
	else:
		return False
def get_wfm(img):
	Xlim, Ylim = img.size
	X = np.linspace(1, Xlim-1, Xlim-1)
	Y = np.linspace(1, Ylim-1, Ylim-1) 
	t, v = [], []
	for x in X:
		for y in Y:
			pixel = get_pixel(img, x, y)
			if pixel == True:
				t.append(x)
				v.append(Ylim - y)
	
	return t,v

def plt_black(img):
	Xlim, Ylim = img.size
	X = np.linspace(1, Xlim-1, Xlim-1)
	Y = np.linspace(1, Ylim-1, Ylim-1)
	t, v = [], []
	for x in X:
		for y in Y:
			pixel = get_black(img, x, y)
			if pixel == True:
				t.append(x)
				v.append(Ylim - y)
	return t, v
	
def cleanup(img, t, v):
	X, Y = img.size
	x = np.linspace(1, Y -1, Y-1)
	time, volts = [], []
	for i in x: 
		temp = []
		for j,k in zip(t, v):
			if i == j:
				try:
					temp.append(k)
				except:
					pass
		if len(temp) != 0:
			y = sum(temp)/len(temp)
			volts.append(y)
			time.append(i)
	#print(time, volts)
	return time, volts

def GetDat(xdiv, ydiv, time, volts):
	# every 50 p is one div
	xinc = xdiv/50
	yinc = ydiv/50
	x = [0]	# set first point to (0,0)
	y = [0]	
	for i in range(len(time)-1):
		x.append((time[i +1] - time[0])*xinc)
	for j in range(len(volts)-1):
		y.append((volts[j + 1] - volts[0]) * yinc)
	return x, y

