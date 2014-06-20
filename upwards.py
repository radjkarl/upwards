# -*- coding: utf-8 -*-
import sys
import os


#from fancytools.io import legalizeValues
from fancytools.utils import question
from fancytools.utils import incrementName

from fancytools.os import PathStr

from configobj import ConfigObj

SAMPLE_PROJECT_STRUCTURE = PathStr(__file__).dirname().join('sample_project_file_structure')
#CONF_FILE_NAME = 'upwards.ini'#'upwards_conf.py'
config = ConfigObj('upwards.ini')
config.initial_comment = [
		"This automtically created file stores all parameters needed for",
		"automated project release and version handling using",
		"python script 'UPWARDS' (see https://pypi.python.org/pypi/upwards)",
		"DO NOT DELETE THIS FILE!"]

auto_args = []
#TODO: auto_args als -a antowrt überall einpflegen - extra def dafür machen??
class FirstTime(object):

	def __init__(self):

		#config = ConfigObj()
		#config.filename = CONF_FILE_NAME


		print('''It seems this is the first time your are using UPWARDS.
	... running first-time-setup...''')
		
		if not question.yn('''Is this your python project directory?
%s
''' %PathStr(os.curdir).tree(0) ):
			sys.exit('Go to yourproject directory and run this script again')

		self.initPypi()
		self.initGithub()
		self.initSphinx()

		self.createProjectStructure()

		d='.'
		dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
		if dirs == '.': #no other dir in this project
			#TODO: file structure test
			sys.exit("""Hmm you don't have sub-directories in your project - that's weird...
		Please have a look at http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
		and ensure that your project structure looks at least like this:
			%s""") %SAMPLE_PROJECT_STRUCTURE.tree()
		#TODO: nicht erforderlich, wenn grad n projekt erstellt wure:, oder?
		config['PROJECTNAME'] = question.number('Whats your projectname', *dirs)
	
		config['VERSION_FILE_NAME'] = question.individual('Where is your version variable stored?',
			os.path.join(config['PROJECTNAME'],'__init__.py'))
	
		config['VERSION_VARIABLE_NAME'] = question.individual(
			'What is the name of the version variable stored in %s?' %config['VERSION_FILE_NAME'],
			'__version__')
	
		print("Please store your version numbers as string, like '0.0.1'")
	
		config.write()




	def initPypi(self):
		c = {}
		c['enabled'] = question.yn('''Do you want to share your project on PyPI
		(https://pypi.python.org)''')
		if c['enabled']:
	
			if question.yn('''Do you allow me to create/modify the PyPI ressource file
				'.pypirc' located in your home directory?
				(see https://docs.python.org/2/distutils/packageindex.html#pypirc)''', True):

				pypyrc = ConfigObj()
				pypyrc.filename = PathStr.home().join('.pypirc')

				pypyrc['distutils'] = {'index-servers':['pypi','test']}


				if not question.yn('''Do you have a PyPI account?'''):#want to save your login details for PyPI in ~/.pypirc
					raw_input('''Than...
			--> go now to https://pypi.python.org and create one.
			--> press any key to continue''')
		
				print('please type in your PyPI ...')
				username = raw_input('username: ')
				password = raw_input('password: ')
				pypyrc['pypi'] = {'repository':'https://pypi.python.org/pypi',
									'username':username,
									'password':password}

				if not question.yn('''Do you have a PyPI-test server account?'''):#want to save your login details for PyPI in ~/.pypirc
					raw_input('''Than...
			--> go now to https://testpypi.python.org/pypi and create one.
			--> press any key to continue''')
		
				print('please type in your PyPI-test server ...')
				username = raw_input('username: ')
				password = raw_input('password: ')
				pypyrc['test'] = {'repository':'https://testpypi.python.org/pypi',
									'username':username,
									'password':password}

				pypyrc.write()

		config['PyPI'] = c


	def initGithub(self):
		c = {}

		c['enabled'] = question.yn('Do you want to share your code on GtHub (https://github.com)')
		if not question.yn('''Do you have a GitHub account?'''):#want to save your login details for PyPI in ~/.pypirc
			raw_input('''Than...
	--> go now to https://github.com/ and create one.
	--> press any key to continue''')

		config['GitHub'] = c


	def initSphinx(self):
		c = {}
		c['doc_via_apidoc'] = question.yn('Do you want to use sphinx-apidoc for your API documentation (http://sphinx-doc.org/man/sphinx-apidoc.html)')
		config['Sphinx'] = c


	def createProjectStructure(self):
		p = SAMPLE_PROJECT_STRUCTURE
		if question.yn('''Do you want me to create the package structure for you?
	This would include...
	%s''' %p.tree() ):
			#create new package folder
			c= PathStr(os.curdir)
			cp = c.parentDir()
			new_project_folder = p.copy(cp.join(
				incrementName( cp.listdir(), p.basename()+'_master') )
				)
			#copy curent dir into new package folder
			#TODO: geht nicht // nicht mehr mit upwars als testproj arbeiten sondern mit tests
			c.copy(new_project_folder)








def inspectArguments():
	'''inspect the command-line-args'''
	args = sys.argv[1:]

	if '-h' in args or '--help' in args:
		sys.exit('TODO') #TODO: write help text
	if '-a' in args:
		pos = args.find('-a')
		for a in args[pos:]:
			if a.startswith('-'):
				break
			auto_args.append(a)
		auto_args = iter(auto_args)



if __name__ == '__main__':

	inspectArguments()
	if not config:
	#value1 = conf['keyword1']
	#try:
	#	import upwards_conf
	#except ImportError:
		FirstTime()

# readConfig():
#	f = open(os.path.join(os.curdir,