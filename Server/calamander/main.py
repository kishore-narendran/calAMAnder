import urllib2, json, datetime, webapp2
from xml.sax.saxutils import unescape
from BeautifulSoup import BeautifulSoup
from google.appengine.api import urlfetch

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

class GetSchedule(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(45)
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
				while "&quot;" in description:
					x = description.find("&quot;")
					description = description[0:x]+description[x+6:len(description)]
				d = readDateTime(date, time)
				ama = {"datetime":str(d), "name":str(name), "description":description}
				soup1 = BeautifulSoup(unicode(tds[i+2]))
				for a in soup1.findAll('a', href = True):
					ama.update({"link":a['href']})
				amas.append(ama)
			self.response.write(json.dumps({"amas":amas, "status":"success"}))
		except urllib2.URLError, e:
			self.response.write(json.dumps({"amas":[], "status":"failure"}))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getschedule', GetSchedule)
], debug=True)
