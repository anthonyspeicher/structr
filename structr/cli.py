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
		print(f'{BLUE}{os.path.basename(os.path.realpath(path))}/{RESET}')
		#var initialization
		indent = '    '
		contents = sorted(os.listdir(path), key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)
		if not show_hidden:
			contents = [i for i in contents if not i.startswith('.')]

		#main - recurse if subdir else print files
		for i in range(len(contents)):
			contents[i] = os.path.join(path, contents[i])
			distance = (os.path.relpath(contents[i], self.args.path)).count(os.sep) + 1

			#print for each file
			print(f'{indent * (distance - (distance - 1))}', end='')
			print('│   ' * (distance - 1), end='')
			if i == len(contents) - 1:
				print(f'└── ', end='')
			else:
				print(f'├── ', end='')

			if os.path.isdir(contents[i]):
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
				elif type != None and str(type).startswith('application/'):
					print(RED, end='')
				elif type != None and str(type).startswith('image/'):
					print(MAGENTA, end='')
				elif type != None and str(type).startswith('audio/'):
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
		#setup - invisible cursor, highlighter initialization
		curses.curs_set(0)
		selected = 0

		while True:
			stdscr.clear()

			#print dirs with highlight
			stdscr.addstr(0, 0, os.path.realpath(path), curses.A_BOLD)
			stdscr.addstr(1, 0, '-' * (len(os.path.realpath(path)) + 8))

			dirs = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
			if not hidden:
				dirs = [i for i in dirs if not i.startswith('.')]
			dirs.sort()

			for x, i in enumerate(dirs):
				if x == selected:
					stdscr.addstr(x + 3, 2, i, curses.A_REVERSE)
				else:
					stdscr.addstr(x + 3, 2, i)

			stdscr.refresh()

			#handle keys
			c = stdscr.getch()

			if c in [curses.KEY_LEFT, ord('j')] and os.path.exists(os.path.dirname(path)):
				path = os.path.dirname(path)
				selected = 0

			elif c in [curses.KEY_ENTER, 10, 13]:
				return path

			if len(dirs) > 0:

				if c in [curses.KEY_UP, ord('l')]:
					selected = (selected - 1) % len(dirs)

				elif c in [curses.KEY_DOWN, ord('k')]:
        	                        selected = (selected + 1) % len(dirs)

				elif c == curses.KEY_PPAGE:
                        	        selected = 0

				elif c == curses.KEY_NPAGE:
        	                        selected = len(dirs) - 1

				elif c in [curses.KEY_RIGHT, ord(';')]:
					path = os.path.join(path, dirs[selected])
					selected = 0

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
			curses.wrapper(lambda stdscr: self.traverse(stdscr, os.path.realpath(self.args.path), self.args.show_hidden))

if __name__ == "__main__":
	structr().main()
