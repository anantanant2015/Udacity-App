from datetime import datetime

from google.appengine.ext import db

import time, json

class Tools(object):
	def RetDateTime(self):
		return datetime.now()

	def RetDateTimeSecondDiff(self, dtime):
		return (datetime.now()-dtime).total_seconds()

	def RetDateTimeDiff(self,dtime):
		#time.sleep(5)
		if dtime:
			return datetime.now()-dtime
		else:
			return datetime.now()

	def RetJson(self, paramdct):
		return json.dumps(paramdct)

	def GetList(self, objectinstance):
		return list(objectinstance)

	def GetListDict(self, objectinstance):
		dct={}			
		List=self.GetList(objectinstance)
		newlist=[]
		for ls in List:
			newlist.append(db.to_dict(ls))
		return newlist