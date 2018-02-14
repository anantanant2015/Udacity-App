import os, webapp2

from classes import Art

from ResponseWrite import jinjaWriter

from GeoPoint import GeoPointLocation

path=os.path.dirname(__file__)

jw=jinjaWriter()

class AsciiChan(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['title']='AsciiChan'
			paramdct['links']='/'
			paramdct['header']='AsciiChan'
			paramdct['footer']='Udacity'
			paramdct['arts']=Art.getarts()
			paramdct['geo_url']='https://maps.googleapis.com/maps/api/staticmap?size=640x640&scale=2'
			gpl=GeoPointLocation()
			gpl.append_marker(paramdct)
			# paramdct['info']=str(paramdct)
			self.response.write(jw.WriteTemplate('asciichan.html', 'website_layout.css', path, **paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
				paramdct['wktemplate']='asciichan.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))


	def post(self):
		try:
			paramdct={}
			paramdct['title']='AsciiChan'
			paramdct['links']='/'
			paramdct['header']='AsciiChan'
			paramdct['footer']='Udacity'
			paramdct['arttitle']=self.request.get('arttitle')
			paramdct['arttxt']=self.request.get('arttxt')
			paramdct['ipaddress']=self.request.remote_addr
			gpl=GeoPointLocation()
			paramdct['geoerror']=gpl.ip_coords(paramdct)
			if paramdct.has_key('latitude') and paramdct.has_key('longitude'):
				paramdct['coords']=gpl.getGeoPoint(paramdct['latitude'], paramdct['longitude'])
			elif paramdct.has_key('lat') and paramdct.has_key('lon'):
				paramdct['coords']=db.GeoPt(paramdct['lat'], paramdct['lon'])
			else:
				paramdct['coords']=None

			if paramdct['arttitle'] and paramdct['arttxt']:
				newart=Art.newart(paramdct['arttitle'], paramdct['arttxt'], paramdct['coords'])
				newart.put()
				self.redirect('/asciichan')
			else:
				paramdct['error']='Both title and art are required!'

			self.response.write(jw.WriteTemplate('asciichan.html', 'website_layout.css', path, **paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
				paramdct['wktemplate']='asciichan.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))



