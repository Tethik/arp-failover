#!/usr/bin/python
import os, sys, subprocess

'''
	Basic executable wrapper for running our C programs.
'''

class Executable(object):
	def __init__(self, path):
		self.executable_path = path
		if(not self.executableExists()):
			raise IOError("Executable not found")

	def executableExists(self):
		return os.path.isfile(self.executable_path)

	def execute(self, *args):
		cargs = list()
		cargs.append(self.executable_path)
		cargs.extend(args)
		p = subprocess.Popen(cargs, stdout=subprocess.PIPE)
		stdout, _ = p.communicate()
		return stdout


if __name__ == "__main__":
	e = Executable("/usr/bin/printenv")
	print(e.execute())
