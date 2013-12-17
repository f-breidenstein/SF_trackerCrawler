#! /usr/bin/env python2

import csv
import getpass
import os
import string
import sys
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup


# Loads all project names from the csv file
# and returns a list
def loadProjectnames():
	projectNames = []
	f = open('projects.csv','r+')
	reader = csv.reader(f,delimiter=',')
	for row in reader:
		projectNames.append(row[0].lower().replace(" ",""))
	f.close()
	return projectNames

# Wants a project name and checks the website
def getTracker(projName):
	tracker = []
	url = "http://sourceforge.net/p/" + projName + "/_list/tickets"
	try:
		response = urllib2.urlopen(url)
		the_page = response.read()
		pool = BeautifulSoup(the_page)
		result = pool.findAll('ul')
		for x in result[len(result)-1]:
			if (unicode(x).find('/p/') != -1):
				tracker.append("http://sourceforge.net/rest" +
								unicode(x).split("href=")[1].split('\"')[1])
	except:
		return tracker

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


# Load Trackerlist from File
def loadTracker(allTracker):
	try:
		g = open('tracker.csv','rb')
	except IOError:
		print "File not found!"
		return

	reader = csv.reader(g)
	for url in reader:
		allTracker.append(url)
	return allTracker

# Run Bicho on every Tracker
# function wants a list with urls, username, password, table name and hostname
def populateDB(allTracker,user,passwd,dbname,hostname):
	username = getpass.getuser()
	cmd = ( "/home/" + username + "/Bicho/bicho --db-hostname-out=" + hostname
		+ " --db-user-out=" + user
		+ " --db-password-out=" + passwd
		+ " --db-database-out=" + dbname
		+ " -d 2 -b allura -u "
		)
	
	for proj in allTracker:
		for line in proj:
			fullCMD = cmd + line
			os.system(fullCMD)

# Check if the project is using the internal Bugtracker
def checkIfUsingSF(projectNames):
	newList = []
	print "Not using Sourceforge:"
	for proj in projectNames:
		tracker = getTracker(proj)
		if (len(tracker) == 0):
			print ">> " + proj
		else:
			newList.append(proj)
	return newList


#####################
# Main program      #
#####################

projectNames = loadProjectnames()
allTracker = []

# Check if the project is using the internal Bugtracker
projectNames = checkIfUsingSF(projectNames)
# TODO: Percent not using Sf tracker

# Get the tracker for every single project in the list
for proj in projectNames:
	allTracker.append(getTracker(proj))

# Write a list of all trackers into a file
writeTracker(allTracker)
#loadTracker(allTracker)

# Run Bicho and write everything to the database
populateDB(allTracker,"root","1234abc","bicho","localhost")

