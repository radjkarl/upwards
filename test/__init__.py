# -*- coding: utf-8 -*-
import os

TEST_FOLDER_NAME = 'upwards_test_project'
SETUP_PROGRAMM_CALL = 'upwards -a 1 2 3 4'
UPDATE_PROGRAMM_CALL = 'upwards -a 1 2 3 4'



def reset():
	pass
	#remove new creates folder
	#delete from test pypi server??


if __name__ == '__main__':
	print('''this test...
	--> a package from the given test folder %s
	--> does the full first-time-setup
	--> send the package to the PyPI test server
	
	to automate all entries the argument '-a' followed by all inputs is added resulting in:
	%s
	''' %(TEST_FOLDER_NAME, SETUP_PROGRAMM_CALL) )
	
	
	os.system(SETUP_PROGRAMM_CALL)
	
	raw_input('''OK - all done! You should now see a new folder, called XXX
	have a look at https://testpypi.python.org/pypi/XXX to see the uploaded project.
	
	PRESS ANY KEY TO CONTINUE''')
	
	print('''At the next stepp we will release a new version 0.0.2 for our package via:
	%s''' %UPDATE_PROGRAMM_CALL)
	
	raw_input('''OK - all done!
	have a look at https://testpypi.python.org/pypi/XXX to see the new version.''')
	
	
	raw_input('''Press any key to end this test and reset all changes''')
	reset()