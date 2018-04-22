import urllib2
import json
import datetime

# get weather information from weather.com.cn
def getWeatherInfo():
	request = urllib2.Request("http://d1.weather.com.cn/sk_2d/101010100.html")
	request.add_header('Referer', 'http://www.weather.com.cn/weather1d/101010100.shtml')

	res = urllib2.urlopen(request)
	jscode = res.read()

	pos = jscode.find('{')
	jsoncode = jscode[pos:]
	jsonobj = json.loads(jsoncode, encoding="UTF-8")
	print("Date: %s, Time: %s, PM25: %s, Temp: %s, Humidity: %s") % (datetime.date.today(), jsonobj['time'], jsonobj['aqi_pm25'], jsonobj['temp'], jsonobj['sd'])

if __name__ == "__main__":
	getWeatherInfo()
