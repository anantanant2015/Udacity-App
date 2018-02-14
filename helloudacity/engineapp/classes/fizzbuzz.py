import os, webapp2

from ResponseWrite import jinjaWriter

path=os.path.dirname(__file__)

jw=jinjaWriter()

class FizzBuzz(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['title']='FizzBuzz'
			paramdct['links']='/'
			paramdct['footer']='Udacity'
			paramdct['header']='FizzBuzz'
			paramdct['n']=self.request.get('n') and int(self.request.get('n'))
			self.response.write(jw.WriteTemplate('fizzbuzz.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='fizzbuzz.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))
