# Anthony Speicher
# 9/22/2025
# CLI tool main file

import os
import argparse
from pathlib import Path
import re
import curses

"""

CUSTOM COLOR SETUP
  Add the file extensions of files you want colored a certain way to
  these lists, "dir" for directories. Example: ".txt"

  To add another color, just add the ASCII color sequence to the color
  variables, a custom list to the color lists starting with your color,
   and your color list to the main list

"""

# colors
BLUE = "\033[34m"
GREEN = "\033[0;32m"
CYAN = "\033[36m"
BOLD_CYAN = "\033[1;36m"
PINK = "\\x1b[38;5;201m"
RED = "\x1b[31m"
MAGENTA = "\x1b[35m"
UNCOLORED = "\033[0m"

# color lists
RED_LIST = [RED, ".tar", ".zip"]
BLUE_LIST = [BLUE, "dir"]
GREEN_LIST = [GREEN, ".exe", ".sh", ".out"]
CYAN_LIST = [CYAN, ".mp3", ".wav", ".aiff", ".wma"]
BOLD_CYAN_LIST = [BOLD_CYAN]
MAGENTA_LIST = [MAGENTA, ".png", ".jpeg", ".jpg", ".gif", ".svg", ".webm", ".mp4"]
PINK_LIST = [PINK]
UNCOLORED_LIST = [UNCOLORED]

# main list
COLORLIST = [RED_LIST, BLUE_LIST, GREEN_LIST, CYAN_LIST, BOLD_CYAN_LIST, MAGENTA_LIST, PINK_LIST, UNCOLORED_LIST]


# main
class structr:
	def __init__(self):
		# argument parsing
		self.parser = argparse.ArgumentParser(prog='structr',
		description='A CLI tool to map, build, and traverse directories.')

		self.parser.add_argument('path', nargs='?', default='.', help='Directory to modify/view')
		self.parser.add_argument('-m', '--map', type=str, metavar='', help='Maps a given directory. Usage: structr -m ../')
		self.parser.add_argument('-b', '--build', type=str, metavar='', help='Builds a given tree from text. Usage: structr -b "<tree>"')
		self.parser.add_argument('-d', '--depth', type=int, default=None, metavar='', help='Sets depth of recursion (default: unlimited). Usage: structr ../ -d 2')
		self.parser.add_argument('--show-hidden', action='store_true', help='Shows or builds dotfiles and hidden folders.')
		self.parser.add_argument('-nc', '--nocolors', action='store_true', help='Disables colors (default: on).  Usage: structr -nc')

	def set_color(self, file):
		# sets text color based on file extension if nocolors option not present
		if not self.args.nocolors:

			# determine filetype
			if os.path.isdir(file):
				extension = "dir"
			else:
				extension = Path(file).suffix

			# change color of text
			for i in COLORLIST:
				if extension in i:
					print(i[0], end="")

	"""
	THIS NEEDS BUG FIXING WITH STRAIGHT LINES WHEN DIRECTORY DOESN'T HAVE FILES
	"""
	def map_tree(self, path, depth, show_hidden):
		self.set_color(path)
		print(f'{os.path.basename(os.path.realpath(path))}/{UNCOLORED}')
		# var initialization
		indent = '    '
		contents = sorted(os.listdir(path), key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)

		#handle hidden dirs and files
		if not show_hidden:
			contents = [i for i in contents if not i.startswith('.')]

		# main - recurse if subdir else print files
		for i in range(len(contents)):
			contents[i] = os.path.join(path, contents[i])
			distance = contents[i].count(os.sep)

			# print for each file
			print(f'{indent * (distance - (distance - 1))}', end='')
			print('│   ' * (distance - 1), end='')
			print('└── ' if i == len(contents) - 1 else '├── ', end='')

			if os.path.isdir(contents[i]):
				if depth and (distance >= depth):
					self.set_color(contents[i])
					print(f'{os.path.basename(contents[i])}/{UNCOLORED}')
				else:
					self.map_tree(contents[i], self.args.depth, self.args.show_hidden)

			else:
				# print file using colors
				self.set_color(contents[i])
				print(f'{os.path.basename(contents[i])}{UNCOLORED}')

	def build_tree(self, build, path, depth, show_hidden):
		# var initialization
		contents = [line for line in build.splitlines() if line.endswith("/")]
		parentdir = contents.pop(0)
		count = 2
		for i in range(len(contents)):

			item = re.sub(r"[├└│─]", " ", contents[i])
			depth = item.count(" ") / 4
			if depth > count:
				count += 1
				parentdir += os.path.basename(re.sub(r"\s+", "", contents[i - 1]).rstrip("/. ")) + "/"

			elif depth < count:
				delete = count - depth
				count = depth
				while delete > 0:
					parentdir = parentdir[:-1]
					if parentdir[-1] == "/":
						delete -= 1

			contents[i] = os.path.join(os.path.join(path, parentdir), item)

		if not show_hidden:
			contents = [i for i in contents if not i.startswith('.')]

                # main - print root, recurse if subdir else print lines then filenames
		for item in contents:
			distance = item.count(" ")
			item = re.sub(r"/\s+", "/", item)
			# print contents/depth check
			os.makedirs(item, exist_ok=True)

	def traverse(self, stdscr, path, hidden):
		# setup - invisible cursor, highlighter initialization
		curses.curs_set(0)
		selected = 0
		dirs = self.makedirs(path, hidden)

		while True:
			stdscr.clear()

			# print dirs with highlight
			stdscr.addstr(0, 0, os.path.realpath(path), curses.A_BOLD)
			stdscr.addstr(1, 0, '-' * (len(os.path.realpath(path)) + 8))

			for x, i in enumerate(dirs):
				if x == selected:
					stdscr.addstr(x + 3, 2, i, curses.A_REVERSE)
				else:
					try:
						self.makedirs(path, hidden)
						stdscr.addstr(x + 3, 2, i)

					except:
						stdscr.addstr(x + 3, 2, f"{RED}{i}{UNCOLORED}")

			stdscr.refresh()

			# handle keys - add any custom keybinds here
			c = stdscr.getch()
			extra = False

			if c in [curses.KEY_LEFT, ord('h')] and os.path.exists(os.path.dirname(path)):
				# sanity check - can't move into nonexistant paths
				if os.path.basename(path):
					dirs = self.makedirs(os.path.dirname(path), hidden)
					selected = dirs.index(os.path.basename(path))
					path = os.path.dirname(path)

			elif c == ord('q'):
				return 0

			elif c in [curses.KEY_ENTER, 10, 13]:
				return path

			if len(dirs) > 0:
				if c == 27:
					extra = True
					screen.nodelay(True)
					c = stdscr.getch()

					if c in [curses.KEY_UP, ord('k')]:
						selected = (selected - 2) % len(dirs)

					elif c in [curses.KEY_DOWN, ord('j')]:
        	                        	selected = (selected + 2) % len(dirs)

				elif c in [curses.KEY_UP, ord('k')]:
					selected = (selected - 1) % len(dirs)

				elif c in [curses.KEY_DOWN, ord('j')]:
					selected = (selected + 1) % len(dirs)

				elif c == curses.KEY_PPAGE:
                        	        selected = 0

				elif c == curses.KEY_NPAGE:
        	                        selected = len(dirs) - 1

				elif c in [curses.KEY_RIGHT, ord('l')]:
					# sanity check - can't move into inaccessible directories
					if self.makedirs(os.path.join(path, dirs[selected]), hidden) != 0:
						path = os.path.join(path, dirs[selected])
						dirs = self.makedirs(path, hidden)
						selected = 0

	def makedirs(self, path, hidden):
		try:
			dirs = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
			if not hidden:
				dirs = [i for i in dirs if not i.startswith('.')]
			dirs.sort()
			return dirs
		except:
			return 0

	def main(self):
		# setup
		self.args = self.parser.parse_args()
		self.args.path = os.path.realpath(self.args.path)
		print()

		# main script
		if self.args.build and self.args.map:
			print("Cannot map and build at the same time.")
			return
		elif self.args.build:
			self.build_tree(self.args.build, self.args.path, self.args.depth, self.args.show_hidden)
		elif self.args.map:
			self.map_tree(self.args.map, self.args.depth, self.args.show_hidden)
		else:
			stdscr = curses.initscr()
			selected_path = curses.wrapper(lambda stdscr: self.traverse(stdscr, os.path.realpath(self.args.path), self.args.show_hidden))
			if not selected_path == 0:
				with open(Path.cwd() / "navigate.sh", "w") as f:
					f.write("#!/bin/bash\n")
					f.write(f"cd {selected_path}\n")
				os.system(f". {os.path.abspath("navigate.sh")}")

def entry():
	structr().main()

if __name__ == "__main__":
	entry()
