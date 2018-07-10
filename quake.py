#!/usr/bin/python

# Written by Dominick Hera
# date: 6/7/18
# email: me@dominickhera.com
# website: www.dominickhera.com
# github: www.github.com/dominickhera


import json
import urllib2
import sys
import datetime

def shiftList(list, newItem, itemIndex):
	tempItem = list.pop(itemIndex)
	list.insert(itemIndex, newItem)
	for i in range(itemIndex+1, len(list), 1):
		list.insert(i, tempItem)
		tempItem = list.pop(i+1)

	return list


if __name__ == "__main__":

	stateArray = [["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District Of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]]
	index = 0
	req = urllib2.Request("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson")
	opener = urllib2.build_opener()
	f = opener.open(req)

	for i in range(1, len(stateArray[0]), 1):
		emptyList = []
		stateArray.append(emptyList)

	json = json.loads(f.read())

	for i in range(0, len(json['features']), 1):

		for j in range(1, len(stateArray[0]), 1):
			if(stateArray[0][j].lower() in json['features'][i]['properties']['place'].lower()):
				earthquakePlace = json['features'][i]['properties']['place']
				earthquakeMag = json['features'][i]['properties']['mag']
				earthquakeTime = json['features'][i]['properties']['time']
				earthquakeDetails = []
				earthquakeDetails.append(earthquakePlace)
				earthquakeDetails.append(earthquakeMag)
				earthquakeDetails.append(earthquakeTime)
				stateArray[j].append(earthquakeDetails)

	print "\n\nEarthquakes per State:\n"
	for i in range(0, len(stateArray[0]), 1):
		print stateArray[0][i], " - Number of Earthquakes: ", len(stateArray[i])

	if(len(sys.argv) > 1):
		if(sys.argv[1].lower() == '--top5'):
			topStates = [[None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None]]
			for i in range(0, len(stateArray[0]) - 1, 1):
					for j in range(0, len(topStates[0]), 1):
						if(len(stateArray[i]) > topStates[2][j] and (stateArray[0][i] in topStates[0]) == False):
							shiftList(topStates[0], stateArray[0][i], j)
							shiftList(topStates[1], i, j)
							shiftList(topStates[2], len(stateArray[i]), j)

			print "\n\nTop 5 US States by Number of Earthquakes:\n"
			for i in range(0, len(topStates[0]), 1):
				print i + 1, topStates[0][i], " - Number of Earthquakes: ", topStates[2][i]
			print '\n'
		else:
			for i in range(0, len(stateArray[0]), 1):
				if(sys.argv[1][2:len(sys.argv[1])].lower() in stateArray[0][i].lower()):
					if(len(stateArray[i]) > 0):
						stateEarthQuakes = [[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
						for k in range(1, len(stateArray[i]) - 1, 1):
							for j in range(0, len(stateEarthQuakes[0]), 1):
								if(stateArray[i][k][1] > stateEarthQuakes[1][j] and (stateArray[i][k][0] in stateEarthQuakes[0]) == False):
									shiftList(stateEarthQuakes[0], stateArray[i][k][0], j)
									shiftList(stateEarthQuakes[1], stateArray[i][k][1], j)
									shiftList(stateEarthQuakes[2], stateArray[i][k][2], j)
						print "\n\nTop",len(stateEarthQuakes[0]), "Earthquakes for the US State:",stateArray[0][i], "\n"
						for i in range(0, len(stateEarthQuakes[0]), 1):
							tempTime = stateEarthQuakes[2][i] / 1000.0
							convertedTime = datetime.datetime.fromtimestamp(tempTime).strftime('%Y-%m-%dT%H:%M:%S.%f')
							print i + 1, "| Location:", stateEarthQuakes[0][i], "| Magnitude:", stateEarthQuakes[1][i], "| Time:", convertedTime, "|"
						print "\n"
					else:
						print stateArray[0][i], "does not have any earthquakes recorded.\n"
