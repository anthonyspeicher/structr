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
		print(f'\n{os.path.basename(os.path.realpath(path))}/')
		for content in os.listdir(path):
			print(f'{os.path.basename(os.path.realpath(content))}/')
			distance = (os.path.relpath(content, path)).count(os.sep)
			if os.path.isdir(content):
				if depth and distance > depth:
					print(f'{content}/')
				else:
					self.map_tree(content, self.args.depth, self.args.show_hidden)
			else:
				print(f'{content}')

	def build_tree(self, build, path, depth, show_hidden):
                print(f'building {build} at {path} with depth {depth}, showhidden = {show_hidden}')

	def main(self):
		#setup
		self.args = self.parser.parse_args()

		#main script
		if self.args.build:
			self.build_tree(self.args.build, self.args.path, self.args.depth, self.args.show_hidden)
		else:
			self.map_tree(self.args.path, self.args.depth, self.args.show_hidden)

if __name__ == "__main__":
	structr().main()
