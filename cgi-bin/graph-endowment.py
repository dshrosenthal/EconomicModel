#!/usr/bin/env python3
import json
import sys
import matplotlib
matplotlib.use('Agg')
import mpl_toolkits.mplot3d.axes3d as p3
import pylab as p
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import requests
import cgi
import cgitb
import re
import tempfile
cgitb.enable()

message = 'Content-Type:text/html' + '\n\n' + '<h1>Endowment Graph</h1>\n<br /><br />'
wwwDir = '/var/www/html'
tempDir = wwwDir + '/images/'

# Other defaults
Duration=100
debug=False
verbose=True
Defaults = '{' + '"DriveCost": "250.0",' + '"SlotCost": "150.0",' + '"SlotTeraByte": "7.2",' + '"SlotCostPerYear": "100.0",' + '"DriveLife": "4",' + '"DriveFailRate": "2",' + '"SlotLife": "8",' + '"DiscountRate": "2",' + '"KryderRate": "10",' + '"SlotRate": "0.0",' + '"LaborPowerRate": "4",' + '"ReplicationFactor": "2"'+ '}'

inputData = json.loads(Defaults)

# Convert POST data to dictionary
def parsePostData(postData):
	global message
	ret = {}
	for p in postData:
		ret[p] = postData[p].value
		if(verbose):
			message = message + "{0} = {1}<br />\n".format(p, ret[p])
	return ret

# Compute endowment for a given DiscountRate and KryderRate
def EndowmentPerTB(x,y):
	# Real interest rate per year
	DiscountRate = x
	# Disk capacity increment per year
	KryderRate = y

	# Initial conditions
	Year=0
	Endowment=0.0
	DiscountFactor=1.0

	if(debug):
		print("inputData: {}<br />\n".format(inputData))
	params = inputData
	# Cost per drive (assumed constant, capacity increases)
	DriveCost = float(params["DriveCost"])
	# Per-slot cost of rack/server/etc
	SlotCost = float(params["SlotCost"])
	# Disk capacity in TB
	SlotTeraByte = float(params["SlotTeraByte"])
	# Annual labor + power cost of a drive slot
	SlotCostPerYear = float(params["SlotCostPerYear"])
	# Service life of drive in years
	DriveLife = int(params["DriveLife"])
	# Annual proportion of drives that fail
	DriveFailRate = float(params["DriveFailRate"])/100.0
	# Service life of rack in years
	SlotLife = int(params["SlotLife"])
	# Real interest rate per year
	#DiscountRate = float(params["DiscountRate"])
	# Disk capacity increment per year
	#KryderRate = float(params["KryderRate"])
	# Rack + server cost decrease per year
	SlotRate = float(params["SlotRate"])
	if(SlotRate >= 1.0):
		SlotRate = SlotRate/100.0
	# Labor + power cost increment per year
	LaborPowerRate = float(params["LaborPowerRate"])
	if(LaborPowerRate >= 1.0):
		LaborPowerRate = LaborPowerRate/100.0
	# Replication factor
	ReplicationFactor = float(params["ReplicationFactor"])
	# Follow the history of a TB
	while(Year<Duration):
		# Incur this year's costs
		Cost = (SlotCostPerYear/SlotTeraByte)
		if(debug):
			print("cost: " + str(Cost) + '<br />')
		if((Year % DriveLife) == 0):
			# Time to replace drive and buy enough spares to
			# cover the (DriveFailRate*DriveLife) of each drive
			# that will fail in service.
			SpareFactor = DriveFailRate*DriveLife
			if(debug):
				print("Spare factor: " + str(SpareFactor) + '<br />')
			Cost += (DriveCost*(1 + SpareFactor)/SlotTeraByte)
			if(debug):
				print("buy disk: " + str(Cost) + '<br />')
		if((Year % SlotLife) == 0):
			# Time to replace rack
			Cost += (SlotCost/SlotTeraByte)
			if(debug):
				print("buy rack: " + str(Cost) + '<br />')
		# Deflate the cost by the discount rate
		Cost *= DiscountFactor
		if(debug):
			print("Discounted: " + str(Cost) + '<br />')
		# Account for replication
		Cost *= ReplicationFactor
		if(debug):
			print("Replicated: " + str(Cost) + '<br />')
		# Add to the endowment
		Endowment += Cost
		if(debug):
			print("Endowment: " + str(Endowment) + '<br />')
		# Adjust costs by the parameters
		SlotTeraByte *= (1.0+KryderRate)
		SlotCost *= (1.0-SlotRate)
		SlotCostPerYear *= (1.0+LaborPowerRate)
		DiscountFactor *= (1.0-DiscountRate)
		Year += 1
	return Endowment

try:
	if(len(sys.argv) > 1):
		inputData = json.loads(sys.argv[1])
		tempDir = '/tmp/'
		wwwDir = tempDir
	else:
		postData = cgi.FieldStorage()
		inputData = parsePostData(postData)
	if(len(inputData) == 0):
		inputData = json.loads(Defaults)
		tempDir = '/tmp/'
		wwwDir = tempDir
	# Discount rate range
	x = np.arange(0.01, 0.11, 0.005)
	# Kryder rate range
	y = np.arange(0.05, 0.25, 0.01)
	X, Y = p.meshgrid(x, y)
	Z = EndowmentPerTB(X, Y)
	fig=p.figure()
	ax = p3.Axes3D(fig)
	surf = ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.coolwarm)
	m = cm.ScalarMappable(cmap=cm.coolwarm)
	m.set_array(Z)
	cbar = plt.colorbar(m, shrink=0.5, aspect=5)
	#fig.colorbar(surf, shrink=0.5, aspect=5)
	ax.set_xlabel('DiscountRate')
	ax.set_ylabel('KryderRate')
	ax.set_zlabel('Endowment$')
	ax.invert_yaxis()
	f = tempfile.NamedTemporaryFile(dir=tempDir, suffix='.png', delete=False)
	fn = f.name[len(wwwDir):len(f.name)]
	plt.savefig(f.name)
	message = message + '<img src="' + fn + '">'
	print(message)
except:
	e = sys.exc_info()
	try:
		message = message + cgitb.text(e)
	except AttributeError:
		message = message + "Got AttributeError: {}\n".format(e)
	print(message)

