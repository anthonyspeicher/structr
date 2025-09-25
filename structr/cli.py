#Anthony Speicher
#9/22/2025
#CLI main file

import os
import argparse
from pathlib import Path
import re

class structr:
	def __init__(self):
		#args
		self.parser = argparse.ArgumentParser(prog='structr',
		description='A CLI tool to map and build trees using text.')
		self.parser.add_argument('path', nargs='?', default='.', help='Directory to map.')
		self.parser.add_argument('-b', '--build', type=str, metavar='', help='Builds a given tree from text. Usage: structr -b "tree"')
		self.parser.add_argument('-d', '--depth', type=int, default=None, metavar='', help='Sets depth of recursion (default: unlimited). Usage: structr . -d 2')
		self.parser.add_argument('--show-hidden', action='store_true', help='Shows dotfiles and hidden folders.')

	def map_tree(self, path, depth, show_hidden):
		#var initialization
		indent = '    '
		contents = sorted(os.listdir(path), key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)
		if not show_hidden:
			contents = [x for x in contents if not x.startswith('.')]

		#main - print root, recurse if subdir else print lines then filenames
		print(f'{os.path.basename(os.path.realpath(path))}/')
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
			if os.path.isdir(contents[i]):
				if depth and (distance >= self.args.depth):
					print(f'{os.path.basename(contents[i])}/')
				else:
					self.map_tree(contents[i], self.args.depth, self.args.show_hidden)
			else:
				print(os.path.basename(contents[i]))

	def build_tree(self, build, path, depth, show_hidden):
		lines = [line for line in build.splitlines() if line.strip()]
		stack = [(path, -1)]  # (path, indent level)

		for idx, line in enumerate(lines):
			indent = len(line) - len(line.lstrip())
			name = re.sub(r"[├└│─]", "", line).strip()
			if not name:
				continue
			if not show_hidden and name.startswith("."):
				continue

            # Determine if this line should be a directory
			is_dir = name.endswith("/")
			if not is_dir:
                # Look ahead: if the next line is more indented, treat as directory
				if idx + 1 < len(lines):
					next_indent = len(lines[idx + 1]) - len(lines[idx + 1].lstrip())
					if next_indent > indent:
						is_dir = True

            # Find parent path based on indentation
			while stack and indent <= stack[-1][1]:
				stack.pop()

			parent_path = stack[-1][0] if stack else path
			full_path = os.path.join(parent_path, name)

			if is_dir:
				Path(full_path).mkdir(parents=True, exist_ok=True)
				stack.append((full_path, indent))
			else:
				Path(full_path).parent.mkdir(parents=True, exist_ok=True)
				Path(full_path).touch()

	def main(self):
		#setup
		self.args = self.parser.parse_args()
		print()

		#main script
		if self.args.build:
			self.build_tree(self.args.build, self.args.path, self.args.depth, self.args.show_hidden)
		else:
			self.map_tree(self.args.path, self.args.depth, self.args.show_hidden)

if __name__ == "__main__":
	structr().main()
