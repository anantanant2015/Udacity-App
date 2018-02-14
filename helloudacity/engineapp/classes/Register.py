from string import letters

import random, hashlib, hmac, webapp2

secret='1234nkij2341^&%@&#@kalfd;,k>:">,./"'

class TaskPassword(object):
	def make_salt(self, length=5):
		return ''.join(random.choice(letters) for x in xrange(length))

	def make_pw_hash(self, name, pw, salt=None):
		if salt==None:
			salt=self.make_salt()
		h=hashlib.sha256(name+pw+salt).hexdigest()
		return '%s,%s'%(salt,h)

	def valid_pw(self, name, password, h):
		salt=h.split(',')[0]
		return h==self.make_pw_hash(name, password, salt)

class TaskCookie(object):
	def login(self, user, Self):
		self.set_secure_cookie('user_id',str(user.key().id()), Self)

	def set_secure_cookie(self, name, val, Self):
		cookie_val=self.make_secure_val(val)
		Self.response.headers.add_header('Set-Cookie', '%s=%s;  Path=/' % (name, cookie_val))

	def make_secure_val(self, val):
		return '%s|%s' % (val, hmac.new(secret,val).hexdigest())

	def initialize(self, User, Self):
		uid=self.read_secure_cookie('user_id', Self)
		Self.user=uid and User.by_id(int(uid))

	def read_secure_cookie(self, name, Self):
		cookie_val=Self.request.cookies.get(name)
		return cookie_val and self.check_secure_val(cookie_val)

	def check_secure_val(self, secure_val):
		val=secure_val.split('|')[0]
		if secure_val==self.make_secure_val(val):
			return val

	def logout(self, Self):
		Self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def render_str(self, template, **params):
		t=jinja_env.get_template(template)
		return t.render(params)	