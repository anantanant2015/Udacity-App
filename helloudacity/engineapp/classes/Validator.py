
import re

dct={}
dct['username']=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
dct['password']=re.compile(r"^.{3,20}$")
dct['email']=re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class validate(object):
	def CheckVal(self,valtype,value,optional,msgname,msgstr,paramdct):
		global dct
		tmp=dct.get(valtype)
		if tmp.match(value)==None and not optional or value!='' and tmp.match(value)==None:
			paramdct[msgname]=msgstr
			paramdct['haserror']=True