
from google.appengine.ext import db

from Register import TaskPassword

class MapCfg(db.Model):
	project=db.StringProperty()
	appkey=db.StringProperty(required=True)

	@classmethod
	def by_get(cls):
		m=MapCfg.all()
		m.order("-appkey")
		m=m.get()
		return m

	@classmethod
	def setkey(cls, appkey, project=None):
		return MapCfg(appkey=appkey, project=project)

class Blog(db.Model):
	subject=db.StringProperty(required=True)
	content=db.TextProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)
	last_modified=db.DateTimeProperty(auto_now=True)

	@classmethod
	def by_fetch(cls, limit=None):
		b=Blog.all()
		b.order("-created")
		b=b.fetch(limit=limit)
		return b

class User(db.Model):
	name=db.StringProperty(required=True)
	phash=db.StringProperty(required=True)
	email=db.StringProperty()

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid)

	@classmethod
	def by_name(cls, name):
		u=User.all()
		u.filter("name =", name)
		u=u.get()
		return u

	@classmethod
	def register(cls, name, pw, email=None):
		tp=TaskPassword()
		pw_hash=tp.make_pw_hash(name, pw)
		return User(name=name, phash=pw_hash, email=email)

	@classmethod
	def login(cls, name, pw):
		tp=TaskPassword()
		u=cls.by_name(name)
		if u and tp.valid_pw(name, pw, u.phash):
			return u

class Art(db.Model):
	title=db.StringProperty(required=True)
	arttxt=db.TextProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)
	coords=db.GeoPtProperty(required=True)

	@classmethod
	def newart(cls, title, arttxt, coords):
		return Art(title=title, arttxt=arttxt, coords=coords)

	@classmethod
	def getarts(cls):
		arts=db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		arts=list(arts)
		return arts

class Wiki(db.Model):
	wkurl=db.StringProperty(required=True)
	content=db.TextProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)

	@classmethod
	def by_id(cls, wid):
		return Wiki.get_by_id(wid)

	@classmethod
	def by_url_get(cls, wkurl):
		w=Wiki.all()
		w.filter("wkurl =", wkurl)
		w.order("-created")
		w=w.get()
		return w

	@classmethod
	def by_url_fetch(cls, wkurl, limit=None):
		w=Wiki.all()
		w.filter("wkurl =", wkurl)
		w.order("-created")
		w=w.fetch(limit=limit)
		return w

	@classmethod
	def newwikiurl(cls, wkurl, content):
		return Wiki(wkurl=wkurl, content=content)
