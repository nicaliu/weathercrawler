import urllib2
import json
import datetime
import MySQLdb
import sys
import sched
import time

# get weather information from weather.com.cn
def getWeatherInfo():
	request = urllib2.Request("http://d1.weather.com.cn/sk_2d/101010100.html")
	request.add_header('Referer', 'http://www.weather.com.cn/weather1d/101010100.shtml')

	res = urllib2.urlopen(request)
	jscode = res.read()

	pos = jscode.find('{')
	jsoncode = jscode[pos:]
	jsonobj = json.loads(jsoncode, encoding="UTF-8")
#	print("Date: %s, Time: %s, PM25: %s, Temp: %s, Humidity: %s") % (datetime.date.today(), jsonobj['time'], jsonobj['aqi_pm25'], jsonobj['temp'], jsonobj['sd'])
	check_wcode(datetime.date.today(), jsonobj)

def check_wcode(date, json):
	sql = "select * from weather_crawl where date='%s'" % date
	dataset = cursor.execute(sql)
	if dataset == 0:
		sql = "insert into weather_crawl(date, time, PM25, temperature, humidity) values('%s', '%s', '%s', '%s', '%s')" % (datetime.date.today(), json['time'], json['aqi_pm25'], json['temp'], json['sd'])
		result = cursor.execute(sql)
		db.commit()
#	else:
#		print("today's weather info exits")

def performAction():
	try:
		getWeatherInfo()
	except Exception as e:
		print e	

	schedule = sched.scheduler(time.time, time.sleep)
	schedule.enter(30, 0, performAction, ())
	print "Starting weather crawler...\n"
	schedule.run()

if __name__ == "__main__":
	db = MySQLdb.connect(host='localhost', 
							user='root', 
							db='test', 
							port=3306)
	cursor = db.cursor()
	performAction()
