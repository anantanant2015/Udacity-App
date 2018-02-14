import os, webapp2

from classes import Blog

from ResponseWrite import jinjaWriter

from CustomTools import Tools

from google.appengine.ext import db

from google.appengine.api import memcache

path=os.path.dirname(__file__)

jw=jinjaWriter()

class BlogHandler(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['links']=['/', '/blog', '/flush']
			paramdct['footer']='Udacity'
			paramdct['autoescape']=False
			path_info=self.request.environ['PATH_INFO']
			template='base.html'
			tl=Tools()

			if path_info=='/flush':
				self.mcflush()
				self.redirect('/blog')

			if path_info=='/blog/newpost':
				template='blognewpost.html'
				paramdct['title']='Blog Newpost'
				paramdct['header']='Blog Newpost'
			elif path_info=='/blog' or path_info=='/blog.json':
				template='blog.html'
				paramdct['title']='Blog'
				paramdct['header']='Blog'
				if self.request.get('postid'):
					paramdct['postid']=self.request.get('postid').split('.')[0]
					# paramdct['posts']=self.getPosts(**paramdct)
					paramdct['mcsearchkey']='P_'+str(paramdct['postid'])
					paramdct['mcpostqtimekey']='PIQT_'+str(paramdct['postid'])
					paramdct['posts']=self.mcoperation(paramdct)
				else:
					#paramdct['posts']=self.getPosts(**paramdct)
					paramdct['mcsearchkey']='PS'
					paramdct['mcpostqtimekey']='PSQT'
					paramdct['posts']=self.mcoperation(paramdct)
				paramdct['mcpostqtime']=self.mctimeget(paramdct)
				paramdct['totalqtime']=str(int(tl.RetDateTimeSecondDiff(paramdct['mcpostqtime'])))+' second/s'
			 
			if path_info.endswith('.json') or self.request.get('postid').endswith('.json'):
			 	paramdct['tojson']=tl.RetJson(list(paramdct['posts']))
			 	self.response.headers['Content-Type']='application/json; charset=UTF-8'
			 	template='base.html'

			if paramdct.has_key('totalqtime'):
				paramdct['info']=paramdct['totalqtime']
			self.response.write(jw.WriteTemplate(template,'website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']=template
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

	def post(self):
		try:
			paramdct={}
			paramdct['links']='/'
			paramdct['title']='Blog'
			paramdct['header']='Blog'
			paramdct['subject']=self.request.get('subject')
			paramdct['content']=self.request.get('content')
			paramdct['autoescape']=False
			if paramdct['subject'] and paramdct['content']:
				bl=Blog(subject=paramdct['subject'], content=paramdct['content'])
				bl.put()
				template='blog.html'
				paramdct['postid']=bl.key().id()
				paramdct['post']=self.getPosts(**paramdct)
				self.redirect('/blog?postid='+str(bl.key().id()))
			else:
				paramdct['error']='Please give the details!'
				template='blognewpost.html'
			self.response.write(jw.WriteTemplate(template,'website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']=template
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

	def getPosts(self,**paramdct):
		if paramdct.has_key('postid')==True:
			posts=Blog.get_by_id(int(paramdct['postid']))
			ls=[]
			if posts!=None:
				posts=self.getDict(posts)
				ls.append(posts)
			return ls
		else:
			# posts=db.GqlQuery("select * from Blog order by created desc limit 10")
			posts=Blog.by_fetch(limit=10)
			tl=Tools()
			return tl.GetList(self.getDict(post) for post in posts)

	def getDict(self, post):
		return {'subject':post.subject,'postid':post.key().id(), 'content':post.content, 'created':post.created.strftime("%a %d %b %y, %I:%M %p"),
			'last_modified':post.last_modified.strftime("%a %d %b %y, %I:%M %p")}

	def mcoperation(self, paramdct):
		if paramdct.has_key('mcsearchkey'):
			result=memcache.get(paramdct['mcsearchkey'])
			if not result:
				result=self.getPosts(**paramdct)
				paramdct['qresult']=result
				paramdct['qaddresult']=self.mcadd(paramdct)
				self.mctimeset(paramdct)
			return result

	def mcadd(self, paramdct):
		result=memcache.add(paramdct['mcsearchkey'], paramdct['qresult'])
		return result

	def mctimeset(self, paramdct):
		tl=Tools()
		result=memcache.set(paramdct['mcpostqtimekey'], tl.RetDateTime())

	def mctimeget(self, paramdct):
		return memcache.get(paramdct['mcpostqtimekey'])

	def mcflush(self):
		return memcache.flush_all()