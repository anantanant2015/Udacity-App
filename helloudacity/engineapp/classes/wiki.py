import os, webapp2

from ResponseWrite import jinjaWriter

from Register import TaskCookie

from classes import User

from classes import Wiki

path=os.path.dirname(__file__)

jw=jinjaWriter()

class WikiHandler(webapp2.RequestHandler):
	def get(self):
		paramdct={}
		try:
			self.initwiki(paramdct)
			
			if paramdct['haserror']==True:
				# paramdct['info']=str(paramdct)
				self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))
			else:
				self.updatedct(paramdct)
				paramdct['info']=str(paramdct)
				self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='wiki.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))


	def post(self):
		paramdct={}
		try:
			self.initwiki(paramdct)
			self.updatedct(paramdct)

			if paramdct['wkedit'] and not paramdct['haserror']:
				paramdct['content']=self.request.get('content')
				if paramdct['content']!=paramdct['contentedit'] or paramdct['isnewurl']:
					w=Wiki.newwikiurl(paramdct['path_info'], paramdct['content'])
					w.put()
					# self.redirect(paramdct['path_info']+'?wkid='+str(w.key().id()))
				# else:
				self.redirect(paramdct['path_info'])
			if paramdct['haserror']:
				self.response.write(jw.WriteTemplate('wiki.html', 'website_layout.css', path, **paramdct))
			else:
				self.redirect(paramdct['path_info'])
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='wiki.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))


	def initwiki(self, paramdct):
		paramdct['links']='/'
		paramdct['title']='Wiki'
		paramdct['wktemplate']='wiki.html'
		paramdct['footer']='Udacity'
		paramdct['path_info']=self.request.environ['PATH_INFO']
		paramdct['haserror']=False
		paramdct['wkedit']=False
		paramdct['iseditpage']=False
		paramdct['ishistorypage']=False
		paramdct['autoescape']=False
		paramdct['isnewurl']=False

		tc=TaskCookie()
		tc.initialize(User, self)
		if self.user:
			paramdct['username']=self.user.name
		else:
			paramdct['haserror']=True

	def updatedct(self, paramdct):
		wk=None
		self.pathfilter(paramdct)
		if not paramdct['haserror']:
			wk=self.geturlwk(paramdct)
		if self.request.get('iseditpage'):
			paramdct['iseditpage']=True
		if wk:
			if paramdct['ishistorypage']:
				paramdct['edit_path_info']='/wiki/edit'+paramdct['path_info']
				paramdct['links']=['/', '/edit', '/logout']
				paramdct['wktemplate']='wikihistory.html'
				paramdct['wk']=wk
			elif paramdct['iseditpage']:
				paramdct['contentedit']=wk.content
				paramdct['wkedit']=True
				paramdct['history_path_info']='/wiki/history'+paramdct['path_info']
				paramdct['links']=['/', '/history', '/logout']
			else:
				paramdct['content']=wk.content
				paramdct['edit_path_info']='/wiki/edit'+paramdct['path_info']
				paramdct['history_path_info']='/wiki/history'+paramdct['path_info']
				paramdct['links']=['/', '/edit', '/history', '/logout']
			

			
			paramdct['info']=str(paramdct)
		else:
			self.newurlwk(paramdct)

	def geturlwk(self, paramdct):
		wk=None
		if self.request.get('wkid'):
			paramdct['wkid']=self.request.get('wkid')
			wk=Wiki.by_id(int(paramdct['wkid']))
		else:
			if paramdct['ishistorypage']:
				wk=Wiki.by_url_fetch(paramdct['path_info'])
				# wk=self.getDict(wk)
			else:
				wk=Wiki.by_url_get(paramdct['path_info'])
		return wk

	def newurlwk(self, paramdct):
		paramdct['wkedit']=True
		paramdct['isnewurl']=True
		if self.request.get('content'):
			paramdct['contentedit']=self.request.get('content')
		else:
			paramdct['contentedit']='Enter content here.'
		paramdct['links']=['/', '/logout']
		paramdct['info']=str(paramdct)

	def pathfilter(self, paramdct):
		if paramdct['path_info'].startswith('/wiki/edit'):
			if paramdct['path_info'].count('/wiki/edit')==1:
				paramdct['path_info']=paramdct['path_info'].replace('/wiki/edit', '')
				paramdct['iseditpage']=True
			else:
				paramdct['error']='Invalid URL/Has "/wiki/edit" in URL!'
				paramdct['haserror']=True
		elif paramdct['path_info'].startswith('/wiki/history'):
			if paramdct['path_info'].count('/wiki/history')==1:
				paramdct['path_info']=paramdct['path_info'].replace('/wiki/history', '')
				paramdct['ishistorypage']=True
			else:
				paramdct['error']='Invalid URL/Has "/wiki/history" in URL!'
				paramdct['haserror']=True

	def getDict(self, wk):
		return {'wkurl':wk.wkurl, 'content':wk.content, 'created':wk.created.strftime("%a %d %b %y, %I:%M %p")}
