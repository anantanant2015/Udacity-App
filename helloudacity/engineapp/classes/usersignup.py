import os, webapp2

from ResponseWrite import jinjaWriter

from Validator import validate

from classes import User

from Register import TaskCookie

path=os.path.dirname(__file__)

jw=jinjaWriter()

vl=validate()

class UserSignUp(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['title']='User SignUp'
			paramdct['links']='/'
			paramdct['footer']='Udacity'
			paramdct['header']='SignUp'
			self.response.write(jw.WriteTemplate('signup.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='signup.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))
		
	def post(self):
		try:
			paramdct={}
			paramdct['footer']='Udacity'
			paramdct['username']=self.request.get('username')
			paramdct['email']=self.request.get('email')
			password=self.request.get('password')
			verifypassword=self.request.get('verifypassword')		
			paramdct['haserror']=False
			vl.CheckVal('username',paramdct['username'],False,'usernameerror','not valid username / username required',paramdct)
			vl.CheckVal('email',paramdct['email'],True,'emailerror','not valid email',paramdct)
			vl.CheckVal('password',password,False,'passworderror','not valid password',paramdct)
			vl.CheckVal('password',verifypassword,False,'verifypassworderror','not valid password',paramdct)
			if password!=verifypassword:
				if paramdct.has_key('verifypassworderror'):
					paramdct['verifypassworderror']=paramdct['verifypassworderror']+' / password did not match'
				else:
					paramdct['verifypassworderror']='password did not match'
				paramdct['haserror']=True

			if self.request.environ['PATH_INFO']=='/signupregister' and paramdct['haserror']==False:
				paramdct['password']=password
				self.registernow(paramdct)
				

			if paramdct['haserror']==False:
				self.redirect('/welcome?username='+paramdct['username'])
			else:
				paramdct['title']='User SignUp'
				paramdct['links']='/'
				paramdct['header']='SignUp'
				paramdct['footer']='Udacity'
				self.response.write(jw.WriteTemplate('signup.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='signup.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

	def registernow(self, paramdct):
		tc=TaskCookie()
		u=User.by_name(paramdct['username'])
		if u!=None:
			paramdct['usernameerror']='Username already exists!'
			paramdct['haserror']=True
		else:
			u=User.register(paramdct['username'], paramdct['password'], paramdct['email'])
			u.put()
			tc.login(u,self)

class UserLogin(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['title']='User Login'
			paramdct['links']='/'
			paramdct['footer']='Udacity'
			paramdct['header']='Login'
			self.response.write(jw.WriteTemplate('login.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='login.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

	def post(self):
		try:
			paramdct={}
			paramdct['footer']='Udacity'
			paramdct['username']=self.request.get('username')
			password=self.request.get('password')
			paramdct['haserror']=False
			vl.CheckVal('username',paramdct['username'],False,'usernameerror','not valid username / username required',paramdct)
			vl.CheckVal('password',password,False,'passworderror','not valid password / password required',paramdct)

			u=User.login(paramdct['username'], password)
			if u==None:
				paramdct['haserror']=True
				paramdct['error']='Invalid Login!'
			else:
				tc=TaskCookie()
				tc.login(u, self)

					
			if paramdct['haserror']==False:
				self.redirect('/cookiewelcome')
			else:
				paramdct['title']='User Login'
				paramdct['links']='/'
				paramdct['header']='Login'
				paramdct['footer']='Udacity'
				self.response.write(jw.WriteTemplate('login.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='login.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

class UserLogout(webapp2.RequestHandler):
	def get(self):
		try:
			tc=TaskCookie()
			tc.logout(self)
			self.redirect('/cookiewelcome')
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='login.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))
