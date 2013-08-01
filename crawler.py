#! /usr/bin/env python2

import urllib
import urllib2
import csv
import string
import sys
import os
from BeautifulSoup import BeautifulSoup


# Loads all project names from the csv file
# and returns a list
def loadProjectnames():
	projectNames = []
	f = open('projects.csv','r+')
	reader = csv.reader(f,delimiter=',')
	for row in reader:
		projectNames.append(row[0])
	f.close()
	return projectNames

# Wants a project name and checks the website 
def gettracker(projName):
	tracker = []
	url = "http://sourceforge.net/p/" + projName + "/_list/tickets"
	response = urllib2.urlopen(url)
	the_page = response.read()
	pool = BeautifulSoup(the_page)
	result = pool.findAll('ul')
	for x in result[2]:
		if (unicode(x).find('/p/') != -1):
			tracker.append("http://sourceforge.net/rest" +
							unicode(x).split("href=")[1].split('\"')[1])
	return tracker

# Write all tracker to a file
# IF THE FILE ALREADY EXISTS IT WILL BE OVERWRITTEN!!
def writeTracker(allTracker):
	g = open('tracker.csv','w')
	writer = csv.DictWriter(g,["url"]) 
	for proj in allTracker:
		for line in proj:
			newRow = {"url" : line}
			writer.writerow(newRow)
	g.close()

# Run Bicho on every Tracker
# function wants a list with urls, username, password, table name and hostname
def populateDB(allTracker,user,passwd,table,hostname):
	cmd = "./bicho -g --db-hostname-out=" + hostname + " --db-user-out=" + user + " --db-password-out=" + passwd + " --db-database-out=" + table + " -d 3 -b allura -u "
	
	for proj in allTracker:
		for line in proj:
			fullCMD = cmd + line
			#print fullCMD
			os.system(fullCMD)

#####################
# Main program
projectNames = loadProjectnames()
allTracker = []

# Get the tracker for every single project in the list 
for proj in projectNames:
	allTracker.append(gettracker(proj))

populateDB(allTracker,"root","1234abc","bicho","localhost")
#writeTracker(allTracker)


# Print out every url for debuging purpose
#for proj in allTracker:
#	for url in proj:
#		print url