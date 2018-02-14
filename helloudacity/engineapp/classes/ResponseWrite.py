import jinja2

import os

path=''
template_dir=''
jinja_env=''


class jinjaWriter(object):
	def WriteTemplate(self,template,style,received_path,**kw):
		global jinja_env
		if jinja_env=='':
			self.init_jinja_env(path, **kw)
		received_style=self.GetTemplate(style)
		temp=self.GetTemplate(template,style=received_style,**kw)
		return temp

	def GetTemplate(self,template,**kw):
		if jinja_env=='':
			self.init_jinja_env(path, **kw)
		t=jinja_env.get_template(template)
		return t.render(kw)

	def init_jinja_env(self,received_path, **kw):
		global path, template_dir, jinja_env
		path=received_path
		template_dir=os.path.join(path,'templates')
		if kw.has_key('autoescape'):
			autoescape=kw['autoescape']
		else:
			autoescape=True
		jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=autoescape)
