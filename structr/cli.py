#Anthony Speicher
#9/22/2025
#CLI main file

import os
import argparse
from pathlib import Path
import re
import filetype
import curses
#import shutil

BLUE = "\033[34m"
GREEN = "\033[0;32m"
CYAN = "\033[36m"
BOLD_CYAN = "\033[1;36m"
PINK = "\\x1b[38;5;201m"
RED = "\x1b[31m"
MAGENTA = "\x1b[35m"
RESET = "\033[0m"


class structr:
	def __init__(self):
		#args
		self.parser = argparse.ArgumentParser(prog='structr',
		description='A CLI tool to map, build, and traverse directories.')
		self.parser.add_argument('path', nargs='?', default='.', help='Directory to modify/view')
		self.parser.add_argument('-m', '--map', type=str, metavar='', help='Maps a given directory. Usage: structr -m ../')
		self.parser.add_argument('-b', '--build', type=str, metavar='', help='Builds a given tree from text. Usage: structr -b "<tree>"')
		self.parser.add_argument('-d', '--depth', type=int, default=None, metavar='', help='Sets depth of recursion (default: unlimited). Usage: structr ../ -d 2')
		self.parser.add_argument('--show-hidden', action='store_true', help='Shows or builds dotfiles and hidden folders.')

	def map_tree(self, path, depth, show_hidden):
		#var initialization
		indent = '    '
		contents = sorted(os.listdir(path), key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)
		if not show_hidden:
			contents = [x for x in contents if not x.startswith('.')]

		#main - print root, recurse if subdir else print lines then filenames
		print(f'{BLUE}{os.path.basename(os.path.realpath(path))}/{RESET}')
		for i in range(len(contents)):
			contents[i] = os.path.join(path, contents[i])
			distance = (os.path.relpath(contents[i], self.args.path)).count(os.sep)

			#print for each file/subdir
			print('│   ' * distance, end='')
			print(f'{indent * (distance - 1)}', end='')
			if i == len(contents) - 1:
				print(f'└── ', end='')
			else:
				print(f'├── ', end='')

			#print contents/depth check
			if os.path.isdir(contents[i]) and not os.path.islink(contents[i]):
				if depth and (distance >= self.args.depth):
					print(f'{BLUE}{os.path.basename(contents[i])}/{RESET}')
				else:
					self.map_tree(contents[i], self.args.depth, self.args.show_hidden)
			else:
				#print file using ls --colors standard
				type = filetype.guess(contents[i])
				if os.path.islink(contents[i]):
					print(BOLD_CYAN, end='')
				#application check - broken currently, can't find good solution
				#elif shutil.which(contents[i]):
					#print(GREEN, end='')
				elif type != None and type.startswith('application/'):
					print(RED, end='')
				elif type != None and type.startswith('image/'):
					print(MAGENTA, end='')
				elif type != None and type.startswith('audio/'):
					print(CYAN, end='')
				print(f'{os.path.basename(contents[i])}{RESET}')

	def build_tree(self, build, path, depth, show_hidden):
#(i for c in list[i] while not c.isalpha())
		#var initialization
		contents = {os.path.join(path, re.sub(r"[├└│─]", "    ", line).strip()):count(i for c in line if not c.isalpha()) for line in build.splitlines() if line.strip()}
		if not show_hidden:
			contents = [x for x in contents if not x.startswith('.')]
		print(contents)

                #main - print root, recurse if subdir else print lines then filenames
		for item in contents:
			distance = (os.path.relpath(item, self.args.path)).count(os.sep)

                        #print contents/depth check
			if item.endswith("/"):
				Path(item).mkdir(parents=True, exist_ok=True)
				if not (depth and (distance >= self.args.depth)):
					self.build_tree(build, item, self.args.depth, self.args.show_hidden)
			else:
				Path(item).touch()

	def traverse(self, stdscr, path, hidden):
		#setup - initial navigation, invisible cursor, initialize dirs list
		os.chdir(os.path.realpath(path))
		curses.noecho()
		curses.cbreak()
		stdscr.keypad(True)
		dirs = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
		dirs.sort()
		print(dirs)

	def main(self):
		#setup
		self.args = self.parser.parse_args()
		print()

		#main script
		if self.args.build:
			self.build_tree(self.args.build, self.args.path, self.args.depth, self.args.show_hidden)
		elif self.args.map:
			self.map_tree(self.args.map, self.args.depth, self.args.show_hidden)
		else:
			stdscr = curses.initscr()
			curses.wrapper(lambda stdscr: self.traverse(stdscr, self.args.path, self.args.show_hidden))

if __name__ == "__main__":
	structr().main()
