from rot13 import Hello

class urlMapper(object):
	def getObject(self,path_info,urlMapping):
		if path_info:
			if path_info=='/':
				obj=Hello()
				urlMappingAppend('/hello',obj,urlMapping)
				return urlMapping
		else:
			return None

def urlMappingAppend(path,objRecieved,urlMapping):
    tu=(path,objRecieved.__class__)
    urlMapping.append(tu)