class ClientSession(object):
	def __init__(self, directory):
		self.directory = directory
		
	def __str__(self):
		return "Current directory is %s" % (self.directory)
	
	def change_directory(self, newDirectory):
		self.directory = newDirectory
