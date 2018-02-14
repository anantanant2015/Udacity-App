import os, webapp2

from ResponseWrite import jinjaWriter

from Validator import validate

from classes import User, MapCfg

from Register import TaskCookie

path=os.path.dirname(__file__)

jw=jinjaWriter()

class MapConfig(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['title']='App Key'
			paramdct['links']='/'
			paramdct['footer']='Udacity'
			paramdct['header']='App Key'
			self.response.write(jw.WriteTemplate('mapconfig.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='mapconfig.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))



	def post(self):
		try:
			paramdct={}
			paramdct['footer']='Udacity'
			paramdct['appkey']=self.request.get('appkey')
			paramdct['haserror']=False	
			paramdct['project']=self.request.get('project')
			paramdct['appkey']=self.request.get('appkey')

			tc=TaskCookie()
			tc.initialize(User, self)
			if self.user:
				paramdct['username']=self.user.name
			else:
				paramdct['haserror']=True

			if paramdct['haserror']==False and paramdct['username']=='Admin_Anant':
				self.updatekeynow(paramdct)
				self.redirect('/asciichan')
			else:
				paramdct['title']='App Key'
				paramdct['links']='/'
				paramdct['footer']='Udacity'
				paramdct['header']='App Key'
				self.response.write(jw.WriteTemplate('mapconfig.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='mapconfig.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

		
	def updatekeynow(self, paramdct):
		tc=TaskCookie()
		m=MapCfg.setkey(paramdct['appkey'], paramdct['project'])
		m.put()
