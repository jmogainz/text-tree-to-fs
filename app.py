import os
import re
import sys

def parse_tree(lines, base_dir='.'):
    stack = []
    prev_indent = -1
    for index, line in enumerate(lines):
        # Remove leading and trailing whitespace
        line = line.rstrip('\n')
        if not line.strip():
            continue  # Skip empty lines

        # Determine the indentation level
        indent_match = re.match(r'^(\s*)(.*)', line)
        indent_space = indent_match.group(1)
        indent = len(indent_space.replace('│', ' ').replace('├', ' ').replace('└', ' ').replace('─', ' ').replace('┬', ' '))
        name = indent_match.group(2).strip()
        name = re.sub(r'^[\│\├\└\─\┬\ ]*', '', name).strip()

        # Remove any trailing '/' from directory names (if present)
        if name.endswith('/'):
            name = name.rstrip('/')

        # Update the stack based on the current indentation
        while stack and indent <= stack[-1][0]:
            stack.pop()

        # Determine if the current line represents a directory
        is_dir = False

        # Peek ahead to see if the next line is more indented (child of current line)
        next_indent = None
        for next_line in lines[index + 1:]:
            next_line = next_line.rstrip('\n')
            if not next_line.strip():
                continue  # Skip empty lines
            next_indent_match = re.match(r'^(\s*)(.*)', next_line)
            next_indent_space = next_indent_match.group(1)
            next_indent = len(next_indent_space.replace('│', ' ').replace('├', ' ').replace('└', ' ').replace('─', ' ').replace('┬', ' '))
            break

        if next_indent is not None and next_indent > indent:
            is_dir = True
        else:
            # Assume it's a file if the name has an extension
            if '.' in name:
                is_dir = False
            else:
                # If there's no extension, we assume it's a directory
                is_dir = True

        current_path = os.path.join(base_dir, *(dir_name for level, dir_name in stack))

        if is_dir:
            # It's a directory
            dir_path = os.path.join(current_path, name)
            os.makedirs(dir_path, exist_ok=True)
            stack.append((indent, name))
        else:
            # It's a file
            if not os.path.exists(current_path):
                os.makedirs(current_path, exist_ok=True)
            file_path = os.path.join(current_path, name)
            with open(file_path, 'w') as f:
                pass  # Creates an empty file

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python create_tree.py <input_file> [<base_dir>]")
        sys.exit(1)

    input_file = sys.argv[1]
    base_dir = sys.argv[2] if len(sys.argv) > 2 else '.'

    # Read lines from the specified input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Parse and create the directory and file structure
    parse_tree(lines, base_dir)

