class ClientSession(object):
	def __init__(self, directory):
		self.home_directory = directory
                self.current_directory = directory
		
	def __str__(self):
		return "Current directory is %s" % (self.directory)
	
	def change_directory(self, newDirectory):
		self.current_directory = newDirectory

        def reset_directory(self):
                self.current_directory = self.home_directory
