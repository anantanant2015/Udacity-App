import logging, os


class WriteLog(object):
	def LogDebug(self,path='',module=''):
		logging.basicConfig(filename='AppLog.txt', level=logging.DEBUG)
		logging.debug(str(path)+str(module))




#logger.error('We have a problem')
#logger.info('While this is just chatty')
