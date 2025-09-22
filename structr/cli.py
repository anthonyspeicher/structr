import os
import argparse

def map_tree():
	pass

def build_tree():
	pass

def main():
	parser = argparse.ArgumentParser(
		prog='structr',
		description='A CLI tool to map and build trees using text.')
	parser.add_argument('-b', '--build', action="store_true", help='Builds a given tree from text. Usage: structr -b <tree>')
	parser.add_argument('--depth', action="store_true", help='Sets depth of recursion for building or reading trees. Usage: structr / --depth <int>')
	parser.print_help()

if __name__ == "__main__":
	main()
