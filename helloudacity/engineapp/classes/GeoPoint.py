import urllib2, json

from classes import MapCfg

from google.appengine.ext import db

# from xml.dom import minidom

url4='http://ip-api.com/json/REPLACEIP'     #150 per minute
url3='http://extreme-ip-lookup.com/json/REPLACEIP'    #200 per minute
url2='http://geoip.nekudo.com/api/REPLACEIP/de/json'   #no limit / may blocked by use
url1='http://freegeoip.net/json/REPLACEIP'   #15000 per hour

urllist=[url1, url2, url3, url4]

class GeoPointLocation(object):
	def ip_coords(self, paramdct):
		try:
			if paramdct.has_key('apiurl') and paramdct.has_key('apiurlopt') and paramdct.has_key('ipaddress'):
				tempurl=paramdct['apiurl'].replace('REPLACEIP',paramdct['ipaddress'])
				paramdct['apiurl']=tempurl
			elif paramdct.has_key('ipaddress'):
				if not paramdct.has_key('apiurlopt'):
					paramdct['apiurlopt']=['latitude', 'longitude', 'lat', 'lon']
			else:
				paramdct['error']='IP address not found!'
			result=self.get_opt(paramdct)
			return result
		except Exception as err:
			paramdct['error']='Location not found!'
			return err

	def get_opt(self, paramdct):
		found=False
		count=0
		try:
			if paramdct.has_key('ipaddress') and paramdct.has_key('apiurlopt'):
				if paramdct.has_key('apiurl'):
					response=urllib2.urlopen(paramdct['apiurl']).read()
					jsresponse=json.loads(response)
					for option in paramdct['apiurlopt']:
							if jsresponse.has_key(option):
								paramdct[option]=jsresponse[option]
								found=True
								count+=1
				else:
					for url in urllist:
						tempurl=url.replace('REPLACEIP',paramdct['ipaddress'])
						response=urllib2.urlopen(tempurl).read()
						jsresponse=json.loads(response)
						for option in paramdct['apiurlopt']:
							if jsresponse.has_key(option):
								paramdct[option]=jsresponse[option]
								found=True
								count+=1
						if found==True and count>1:
							break
			return found
		except Exception as err:
			return err

	def append_marker(self, paramdct):
		self.getartcoords(paramdct)
		if paramdct.has_key('geo_url') and paramdct.has_key('artcoords'):
			markers=''.join('&markers=color:red|label:S|%s,%s' % (a.lat, a.lon) for a in paramdct['artcoords'])
			paramdct['geo_url']+=markers
			self.append_key(paramdct)

	def getappkey(self, paramdct):
		key=MapCfg.by_get()
		if key:
			paramdct['appkey']=key.appkey
			# paramdct['info']='Key from db, "'+str(key.appkey)+'"'

	def append_key(self, paramdct):
		self.getappkey(paramdct)
		if paramdct.has_key('appkey'):
			paramdct['geo_url']+='&key='+paramdct['appkey']
		else:
			paramdct['geo_url']+='&key=AIzaSyDWn6DNHZExBEhjyWo0hA1RPs-a5SDVrv8'

	def getartcoords(self, paramdct):
		if paramdct.has_key('arts'):
			paramdct['artcoords']=filter(None, (a.coords for a in paramdct['arts']))

	def getGeoPoint(self, lat, lon):
		return db.GeoPt(lat, lon)




# url=urllib2.urlopen('http://freegeoip.net/xml/4.2.2.2')
# j=url.read()
# d=minidom.parseString(j)

# x=json.loads(j)
# x.has_key('latitude')
# x['latitude']
# x['longitude']
