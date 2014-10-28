'''
Created on Oct 23, 2014

@author: alejandro
'''

import os.path
import csv

	
def verifyFile(path):
	return os.path.exists(path)


def readFile(path):
	result = []
	with open(path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			result.append(row)
	return result

	
def writeFile(path, obj):
	try:
		f = open(path, 'w')
		for row in obj:
			f.write(row + "\n")
		f.close()
		return True
	except:
		return False