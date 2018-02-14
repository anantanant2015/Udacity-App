import os, webapp2

from ResponseWrite import jinjaWriter

path=os.path.dirname(__file__)

jw=jinjaWriter()

class ShoppingList(webapp2.RequestHandler):
	def get(self):
		try:
			paramdct={}
			paramdct['title']='Shopping List'
			paramdct['links']='/'
			paramdct['food']=filter(lambda x:x!='',self.request.get_all('food'))
			paramdct['header']='Shopping List'
			paramdct['footer']='Udacity'
			self.response.write(jw.WriteTemplate('shoppinglist.html','website_layout.css',path,**paramdct))
		except Exception as err:
			if paramdct.has_key('error'):
				paramdct['error']+=', ' + str(err)
			else:
				paramdct['error']=err
			paramdct['wktemplate']='shoppinglist.html'
			self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))
