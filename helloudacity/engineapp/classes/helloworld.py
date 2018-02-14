
import webapp2, os

from ResponseWrite import jinjaWriter

jw=jinjaWriter()

path=os.path.dirname(__file__)

class HelloWorld(webapp2.RequestHandler):
    def get(self):
    	paramdct={}
    	if self.request.get('q'):
    		q=self.request.get('q')
    	else:
    		q='Hello World'
    	paramdct['title']=q
    	paramdct['links']='/'
    	paramdct['text']=q
    	paramdct['header']=q
    	paramdct['footer']='Udacity'
        self.response.write(jw.WriteTemplate('helloworld.html','website_layout.css',path,**paramdct))