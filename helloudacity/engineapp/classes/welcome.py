
import os, webapp2

from ResponseWrite import jinjaWriter

from Validator import validate

from Register import TaskCookie

from classes import User

path=os.path.dirname(__file__)

jw=jinjaWriter()

vl=validate()

class Welcome(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['haserror']=False
			if self.request.environ['PATH_INFO']=='/cookiewelcome':
				tc=TaskCookie()
				tc.initialize(User, self)
				self.welcome(paramdct)
			else:
				paramdct['username']=self.request.get('username')
				vl.CheckVal('username',paramdct['username'],False,'usernameerror','username not valid',paramdct)

			if paramdct['haserror']==False:
				paramdct['title']='Welcome'
				paramdct['links']='/'
				self.response.write(jw.WriteTemplate('welcome.html','website_layout.css',path,**paramdct))
			else:
				self.redirect('/signup')
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
				paramdct['wktemplate']='welcome.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))


	def welcome(self, paramdct):
		if self.user:
			paramdct['username']=self.user.name
		else:
			paramdct['haserror']=True

