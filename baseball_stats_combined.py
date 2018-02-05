###############################################################################
# Script to combine baseball stats from multiple .csv files
# Author: Bo Adams
# Date: 2/5/2018
###############################################################################

import sys


def parseCSVMaster(filename):
	f = open(filename)
	data = f.readlines()
	masterList = []
	skipLine = 0
	for line in data:
		if skipLine != 0:	
			playerID, birthYear, birthMonth, birthDay, birthCountry, birthState, birthCity, deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, debut, finalGame, retroID, bbrefID = line.split(",")
			dataLine = [playerID, birthMonth, birthCountry, weight, height, bats, throws, nameFirst, nameLast]
			masterList.append(dataLine)
		skipLine = skipLine + 1
	return masterList

def parseCSVBatting(filename):
	f = open(filename)
	data = f.readlines()
	battingList = []
	skipLine = 0
	for line in data:
		if skipLine != 0:
			playerID, yearID, stint, teamID, lgID, G, AB, R, H, twoB, threeB, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP = line.split(",")
			dataLine = [playerID, yearID, stint, teamID, lgID, G, AB, R, H, twoB, threeB, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP]
			battingList.append(dataLine)
		skipLine = skipLine + 1
	return battingList

def parseCSVSalary(filename):
	f = open(filename)
	data = f.readlines()
	salaryList = []
	skipLine = 0
	for line in data:
		if skipLine != 0:
			yearID, teamID, lgID, playerID, salary = line.split(",")
			dataLine = [playerID, yearID, teamID, salary]
			salaryList.append(dataLine)
		skipLine = skipLine + 1
	return salaryList

def parseCSVAwards(filename):
	f = open(filename)
	data = f.readlines()
	awardList = []
	skipLine = 0
	for line in data:
		if skipLine != 0:
			playerID, awardID, yearID, lgID, tie, notes = line.split(",")
			dataLine = [playerID, yearID, awardID, tie]
			awardList.append(dataLine)
		skipLine = skipLine + 1
	return awardList

def getBattersFromList(dataList, battingList):
	dataInfo = []
	for batterIndex in range(0, len(battingList)):
		batterFound = False
		for statLine in dataList:
			if battingList[batterIndex][0] == statLine[0] and battingList[batterIndex][1] == statLine[1]:
				infoLine = []
				infoLine.append(batterIndex)
				for i in range(2, len(statLine)):
					infoLine.append(statLine[i])
				dataInfo.append(infoLine)
				batterFound = True
		if batterFound == False:
			infoLine = [batterIndex, "", ""]
			dataInfo.append(infoLine)
	return dataInfo

def combineData(currentList, listToAdd):
	for item in listToAdd:
		entryIndex = item[0]
		if len(currentList[entryIndex]) < 26:
			for i in range(1, len(item)):
				currentList[entryIndex].append(item[i])

def getBatterInfo(master, batters):
	for yearPlayer in batters:
		for player in master:
			if yearPlayer[0] == player[0]:
				for i in range(1, len(player)):
					yearPlayer.append(player[i])

def formatCSV(listToFormat):
	listToWrite = []
	firstLine = "playerID,yearID,stint,teamID,lgID,G,AB,R,H,twoB,threeB,HR,RBI,SB,CS,BB,SO,IBB,HBP,SH,SF,GIDP,teamID,salary,awardID,tie,birthMonth,birthCountry,weight,height,bats,throws,nameFirst,nameLast"
	listToWrite.append(firstLine)
	for dataLine in listToFormat:
		textLine = ""
		for dataPoint in dataLine:
			textLine = textLine + str(dataPoint).rstrip() + ","

		listToWrite.append(textLine)
	return listToWrite

def writeCSV(textToWrite, filenameToWrite):
	with open(filenameToWrite, 'w') as f:
		for line in textToWrite:
			f.write(line)
			f.write("\n")

def main():
	filename1 = sys.argv[1]
	filename2 = sys.argv[2]
	filename3 = sys.argv[3]
	filename4 = sys.argv[4]
	outputname = sys.argv[5]
	if(filename1 == outputname):
		raise AssertionError('Input filename cannot be the same as output filename')
	if(filename2 == outputname):
		raise AssertionError('Input filename cannot be the same as output filename')
	if(filename3 == outputname):
		raise AssertionError('Input filename cannot be the same as output filename')
	masterList = parseCSVMaster(filename1)
	print("Master has been read")
	salaryList = parseCSVSalary(filename2)
	print("Salaries have been read")
	battingList = parseCSVBatting(filename3)
	print("Batting Stats have been read")
	awardsList = parseCSVAwards(filename4)
	print("Awards have been read")
	salariesToAdd = getBattersFromList(salaryList, battingList)
	csvList = battingList
	combineData(csvList, salariesToAdd)
	print("Salaries added")
	awardsToAdd = getBattersFromList(awardsList, battingList)
	combineData(csvList, awardsToAdd)
	print("Awards Added")
	getBatterInfo(masterList, csvList)
	print("Added Master Data")
	textToWrite = formatCSV(csvList)
	print("Writing CSV")
	writeCSV(textToWrite, outputname)

	#print(countList)
	#textToWrite = getCSVFormatList(countList)
	#writeCSV(textToWrite, filename2)

	#print(relevantData)
	#substrateCountList = []
	#getSubstrateCounts(countList, substrateCountList)
	#print(substrateCountList)

if __name__ == '__main__':
	main()