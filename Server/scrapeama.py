import urllib2, json
import datetime
from BeautifulSoup import BeautifulSoup

def readDateTime(date, time):
	today = datetime.date.today()
	month = date[len(date)-3 : len(date)]
	monthno = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
	day = date[0:len(date)-3]
	apm = time[len(time)-2:len(time)]
	time = time[0:len(time)-2]
	hour = minute = 0
	if len(time)>2:
		minute = time[len(time)-2:len(time)]
		hour = time[0:time.find(':')]
	else:
		hour = time
		minute = 0
	hour = int(hour)
	minute = int(minute)
	day = int(day)
	if apm == 'pm' and hour is not 12:
		hour = hour + 12
	d = datetime.datetime(year = today.year, month = monthno[month], day = day, hour = hour, minute = minute)
	return d

url = "http://www.reddit.com/r/iama"
try:
	result = urllib2.urlopen(url)
	result = result.read()
	soup = BeautifulSoup(result)
	tables = soup.findAll('table')
	soup = BeautifulSoup(unicode(tables[0]))
	tds = soup.findAll('td')
	amas = []
	for i in range(0, len(tds), 4):
		date = tds[i].text
		time = tds[i + 1].text
		name = tds[i + 2].text
		description = tds[i + 3].text
		d = readDateTime(date, time)
		ama = {"datetime":str(d), "name":name, "description":description}
		soup1 = BeautifulSoup(unicode(tds[i+2]))
		for a in soup1.findAll('a', href = True):
			ama.update({"link":a['href']})
		amas.append(ama)
	print(json.dumps({"amas":amas}))

except urllib2.URLError, e:
	print 'Error'
