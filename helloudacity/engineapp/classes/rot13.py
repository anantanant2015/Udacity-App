import webapp2, os

from ResponseWrite import jinjaWriter

from CustomTools import Tools

form="""<!DOCTYPE html><html><head><title>ROT13</title></head><body><form method=post>
<div style="font-size:50px;color: #6746b4;background-color: #b0c4de7d;font-style: italic;">Enter Text for ROT13...</div>
<textarea name="txtarea" style="height:400px;width:100%;">%s</textarea>
<input type="submit">
</form></body></html>"""

params=''
dtime=''

jw=jinjaWriter()
lnDrot=0
Drot={}
path=os.path.dirname(__file__)

class rot(webapp2.RequestHandler):
    def WriteResponse(self,params):
        tools=Tools()
        global dtime
        self.response.write(form.replace('%s',cgi.escape(params,quote=True))+'lnDrot=%s'%lnDrot+' lnitxt=%s'%str(len(params))+ ' datetime=%s'%tools.RetDateTime()+' datetimediff=%s'%tools.RetDateTimeDiff(dtime))
    
    def get(self):
        try:
            paramdct={}
            paramdct['title']='ROT13'
            paramdct['links']='/'
            paramdct['header']='ROT13'
            paramdct['footer']='Udacity'
            global path
            self.response.write(jw.WriteTemplate('rot13.html','website_layout.css',path,**paramdct))
        except Exception as err:
            if paramdct.has_key('error'):
                paramdct['error']+=', ' + str(err)
            else:
                paramdct['error']=err
            paramdct['wktemplate']='rot13.html'
            self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))


    def post(self):
        try:
            global dtime
            tools=Tools()
            paramdct={}
            paramdct['title']='ROT13'
            paramdct['links']='/'
            paramdct['header']='ROT13'
            paramdct['footer']='Udacity'
            dtime=tools.RetDateTime()
            x=self.request.get('txtarea')
            if x:
                paramdct['txt']=self.GetRot13(x,len(x))
            else:
                paramdct['txt']=''
            
            # self.response.write(dtime)
            # del dtime
            # try:
                # self.response.write(dtime)
            # except Exception as err:
            #     x=rot()
            #     paramdct['error']=err
                # self.response.write(' Exception Name=%s and Exception=%s and Class=%s'%(type(err).__name__,err,x.__class__.__name__))
                # self.response.write('HTTP_ORIGIN=%s'% self.request.environ['HTTP_ORIGIN'])
                # self.response.write('HTTP_HOST=%s'% self.request.environ['HTTP_HOST'])
                # self.response.write('PATH_INFO=%s'% self.request.environ['PATH_INFO'])
            # paramdct['info']='HTTP_ORIGIN='+self.request.environ['HTTP_ORIGIN']+' HTTP_HOST='+self.request.environ['HTTP_HOST']+' PATH_INFO='+\
            #     self.request.environ['PATH_INFO']+' DateTime='+str(dtime)+' Processing Time='+str(tools.RetDateTimeDiff(dtime))
            paramdct['info']=dtime.strftime("%a %d %b %y, %I:%M %p")+' Processing Time='+str(tools.RetDateTimeDiff(dtime))

            self.response.write(jw.WriteTemplate('rot13.html','website_layout.css',path,**paramdct))
        except Exception as err:
            if paramdct.has_key('error'):
                paramdct['error']+=', ' + str(err)
            else:
                paramdct['error']=err
            paramdct['wktemplate']='rot13.html'
            self.response.write(jw.WriteTemplate(paramdct['wktemplate'], 'website_layout.css', path, **paramdct))

            
    def GetRot13(self,itxt,lnitxt):
        itx=''
        global lnDrot
        if lnDrot==0:
            self.DRot13(ord('a'),ord('z'))
            self.DRot13(ord('A'),ord('Z'))
            lnDrot=len(Drot)
        for idx in range(lnitxt):
            if Drot.has_key(itxt[idx]):
                itx+=Drot.get(itxt[idx])
            else:
                itx+=itxt[idx]
        return itx

    def DRot13(self,first,last):
        for a in range(first,last+1):
            if ((a+13) <= last):
                Drot[chr(a)]=chr(a+13)
            else:
                Drot[chr(a)]=chr(a-13)