#!/lusr/bin/python

import cProfile
import os
import sys

def main ():
# Get the directory from the command line
	try:
		directory = sys.argv[1]
		directory = os.path.abspath(directory)
	except IndexError:
		directory = '/v/filer4b/v41q001/downing/public_html/projects/netflix/'

# Read the probe data
	file = os.path.join(directory, 'probe.txt')
	file = open(file, 'r')
	file.readlines()
	file.close()

# Read the movie data
	file = os.path.join(directory, 'movie_titles.txt')
	file = open(file, 'r')
	file.readlines()
	file.close()

# Read the training data
	directory = os.path.join(directory, 'training_set/')
	files = os.listdir(directory)
	for file in files:
		file = os.path.join(directory, file)
		file = open(file, 'r')
		file.readlines()
		file.close()

if __name__ == '__main__':
	#cProfile.run('main()')
	main()
