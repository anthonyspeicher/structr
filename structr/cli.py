#Anthony Speicher
#9/22/2025
#CLI main file

import os
import argparse

class structr:
	def __init__(self):
		self.parser = argparse.ArgumentParser(prog='structr',
		description='A CLI tool to map and build trees using text.')
		self.parser.add_argument('path', nargs='?', default='.', help='Directory to map.')
		self.parser.add_argument('-b', '--build', type=str, metavar='', help='Builds a given tree from text. Usage: structr -b <tree>')
		self.parser.add_argument('-d', '--depth', type=int, default=None, metavar='', help='Sets depth of recursion (default: unlimited). Usage: structr / -d 2')
		self.parser.add_argument('--show-hidden', action='store_true', help='Shows dotfiles and hidden folders.')

	def map_tree(self, path, depth, show_hidden):
		pass

	def build_tree(self, path, depth, show_hidden):
		pass

	def main(self):
		#setup
		args = self.parser.parse_args()

		#main script
		if args.build:
			self.build_tree(args.path, args.depth, args.show_hidden)
		else:
			self.map_tree(args.path, args.depth, args.show_hidden)

if __name__ == "__main__":
	structr().main()
