from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import ssl
import csv
import time
from datetime import datetime

# Gangstas Only: Not checking ssl certification

ssl._create_default_https_context = ssl._create_unverified_context

my_url = "https://realclearpolitics.com/epolls/latest_polls/"

# opening up connnection, grabbing the page

uClient = uReq(my_url)

# offloads connection content into a variable

page_html = uClient.read()

# closes connection

uClient.close()

# html parsing

page_soup = soup(page_html, "html.parser")

# grabs each product

races = page_soup.findAll("td", {"class":"lp-race"})
raceC = page_soup.findAll("td", {"class":"lp-race"})
polls = page_soup.findAll("td", {"class":"lp-poll"})
results = page_soup.findAll("td", {"class":"lp-results"})
spreads = page_soup.findAll("td", {"class":"lp-spread"})
dates = page_soup.findAll("td", {"class":"date"})
tables = page_soup.findAll("table", {"class":"sortable"})


# Opens an output file to write to, writes header
file_object = open("RCPinfo.txt", "w")
file_object.write('%-70s %-35s %-95s %-30s %-30s\n\n' % ("Race Name", "Poll Name", "Poll Results", "Poll Spread", "Date"))


pollCountList = []
mapList = []

# append the number of races in this table
for table in tables:
	names = table.findAll('td', {"class":"lp-race"})
	pollCountList.append(len(names))

rowNum = len(raceC)
var = len(pollCountList)

# We loop through the total number of polls
# for every poll we create a map for the table of the poll

for y in range(0, var):
	c = 0
	while c < pollCountList[y]:
		mapList.append(y)
		c = c + 1

dateList = []

# append all the dates to a list
for date in dates:
	dateList.append(date.string);

# list to hold current list of scraped polls
allPolls = []
# list to hold the current polls in the csv
oldPolls = []

# Takes date format like: Wednesday, February 7
# transforms into format DD/MM/YYYY
def formatDate (str):
	date = ""
	a,b = str.split(',')
	del a
	space,month,day = b.split(' ')
	del space

	if month == "January":
		date = date + "01/"
	if month == "February":
		date = date + "02/"
	if month == "March":
		date = date + "03/"
	if month == "April":
		date = date + "04/"
	if month == "May":
		date = date + "05/"
	if month == "June":
		date = date + "06/"
	if month == "July":
		date = date + "07/"
	if month == "August":
		date == date + "08/"
	if month == "September":
		date = date + "09/"
	if month == "October":
		date = date + "10/"
	if month == "November":
		date = date + "11/"
	if month == "December":
		date = date + "12/"

	date = date + day + "/"

	year = datetime.now().strftime('%Y')

	date = date + year

	return date

# Take as input: Democrats 44, Republicans 39
# Transform to a simple decimal value
def formatDem (str):
	result = ""
	Dem,Rep= str.split(',')
	a,DemP,c,RepP=str.split(' ')
	del a
	del c
	Score,comma=DemP.split(',')
	del comma
	Score = "." + Score
	return Score

def formatRep (str):
	result = ""
	Dem,Rep= str.split(',')
	a,DemP,c,RepP=str.split(' ')
	del a
	del c
	RepP = "." + RepP
	return RepP

# list to hold the dates of the polls currently in the csv
oldDates = []

# append all of the dates into oldDates
with open("outputFile.csv", "r", encoding="utf8") as fp:
	reader = csv.reader(fp)
	for row in reader:
		if (len(row) > 0):
			oldDates.append(row[0])	
	
# find the most recent date in the current csv
max = oldDates[-1]


for count in range(0, rowNum):
	raceName = races[count].a.string
	pollName = polls[count].a.string
	pollSpread = spreads[count].span.string
	pollResult = results[count].a.string

	pollDate = dateList[mapList[count]]
	pollDate = formatDate(pollDate)

	if raceName == "2018 Generic Congressional Vote":
		RepScore = formatRep(pollResult)
		DemScore = formatDem(pollResult)

		pollInstance = [pollDate, DemScore, RepScore, pollName, raceName]
		allPolls.append(pollInstance)

# reverse so that the data gets input with oldest at bottom and newest at top
allPolls.reverse()

# write new polls to the csv
with open("outputFile.csv", "a", newline='') as f:
	writer=csv.writer(f, delimiter=',')
	for poll in allPolls:
		pollDate1 = time.strptime(poll[0], "%m/%d/%Y")
		max1 = time.strptime(max, "%m/%d/%Y")
		if pollDate1 > max1:
			writer.writerow(poll)


file_object.close()

# test file for only the most recent polls
with open("example.csv", "w", newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	for poll in allPolls:
		writer.writerow(poll)
