#!/usr/bin/env python3

import requests
import json
import cgi
import cgitb
import sys
import re
cgitb.enable()

message = 'Content-Type:text/html' + '\n\n' + '<h1>Endowment</h1>\n<br /><br />'

import json

# Other defaults
Duration=100
debug=False
Defaults = '{' + '"DriveCost": "250.0",' + '"SlotCost": "150.0",' + '"SlotTeraByte": "7.2",' + '"SlotCostPerYear": "100.0",' + '"DriveLife": "4",' + '"DriveFailRate": "2",' + '"SlotLife": "8",' + '"DiscountRate": "2",' + '"KryderRate": "10",' + '"SlotRate": "0.0",' + '"LaborPowerRate": "4",' + '"ReplicationFactor": "1"' + '}'

# Convert POST data to dictionary
def parsePostData(postData):
	ret = {}
	for p in postData:
		ret[p] = postData[p].value
	return ret

# Compute endowment from a set of parameters as a dictionary
def EndowmentPerTB(params):
	# Initial conditions
	Year=0
	Endowment=0.0
	DiscountFactor=1.0
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
	DiscountRate = float(params["DiscountRate"])/100.0
	# Disk capacity increment per year
	KryderRate = float(params["KryderRate"])/100.0
	# Rack + server cost decrease per year
	SlotRate = float(params["SlotRate"])/100.0
	# Labor + power cost increment per year
	LaborPowerRate = float(params["LaborPowerRate"])/100.0
	# Replication factor
	ReplicationFactor = float(params["ReplicationFactor"])

	# Follow the history of a TB
	while(Year<Duration):
		# Incur this year's costs
		Cost = (SlotCostPerYear/SlotTeraByte)
		if(debug):
			print("cost: " + str(Cost))
		if((Year % DriveLife) == 0):
			# Time to replace drive and buy enough spares to
			# cover the (DriveFailRate*DriveLife) of each drive
			# that will fail in service.
			SpareFactor = DriveFailRate*DriveLife
			if(debug):
				print("Spare factor: " + str(SpareFactor))
			Cost += (DriveCost*(1 + SpareFactor)/SlotTeraByte)
			if(debug):
				print("buy disk: " + str(Cost))
		if((Year % SlotLife) == 0):
			# Time to replace rack
			Cost += (SlotCost/SlotTeraByte)
			if(debug):
				print("buy rack: " + str(Cost))
		# Deflate the cost by the discount rate
		Cost *= DiscountFactor
		if(debug):
			print("Discounted: " + str(Cost))
		# Account for replication
		Cost *= ReplicationFactor
		if(debug):
			print("Replicated: " + str(Cost) + '<br />')
		# Add to the endowment
		Endowment += Cost
		if(debug):
			print("Endowment: " + str(Endowment))
		# Adjust costs by the parameters
		SlotTeraByte *= (1.0+KryderRate)
		SlotCost *= (1.0-SlotRate)
		SlotCostPerYear *= (1.0+LaborPowerRate)
		DiscountFactor *= (1.0-DiscountRate)
		if(debug):
			print("SlotTeraByte: " + str(SlotTeraByte))
			print("SlotCost: " + str(SlotCost))
			print("SlotCostPerYear: " + str(SlotCostPerYear))
			print("DiscountFactor: " + str(DiscountFactor))
		Year += 1
	return Endowment

try:
	inputData = json.loads(Defaults)
	if(len(sys.argv) > 1):
		inputData = json.loads(sys.argv[1])
	else:
		postData = cgi.FieldStorage()
		inputData = parsePostData(postData)
	if(len(inputData) == 0):
		inputData = json.loads(Defaults)
	result = EndowmentPerTB(inputData)
	message = message + "Endowment = $" + ('%.2f' % result) + '<br />'
except:
	e = sys.exc_info()
	try:
		message = message + cgitb.text(e)
	except AttributeError:
		message = message + "Got AttributeError: {}\n".format(e)
		
print(message)
