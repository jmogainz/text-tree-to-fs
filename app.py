import os
import re
import sys

def get_indent_level(line):
    # Remove newline and trailing whitespace
    line = line.rstrip('\n')
    # Match leading tree characters and spaces
    match = re.match(r'^([\s\│\├\└\─]*)(.*)', line)
    leading_chars = match.group(1)
    rest_line = match.group(2)
    # Each indentation level is represented by 4 characters
    indent_level = len(leading_chars) // 4
    # Remove leading tree characters and spaces from the name
    name = re.sub(r'^[\│\├\└\─\ ]+', '', rest_line).strip()
    return indent_level, name

def parse_tree(lines, base_dir='.'):
    stack = []
    for index, line in enumerate(lines):
        line = line.rstrip('\n')
        if not line.strip():
            continue  # Skip empty lines

        indent, name = get_indent_level(line)

        if not name:
            continue  # Skip lines that don't contain a name

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
            next_indent, _ = get_indent_level(next_line)
            break

        if next_indent is not None and next_indent > indent:
            is_dir = True
        else:
            # Assume it's a file if the name has an extension
            if '.' in name or '*' in name:
                is_dir = False
            else:
                # If there's no extension, we assume it's a directory
                is_dir = True

        # Build the current path
        current_dirs = [dir_name for level, dir_name in stack]
        current_path = os.path.join(base_dir, *current_dirs)

        if is_dir:
            # It's a directory
            dir_path = os.path.join(current_path, name)
            os.makedirs(dir_path, exist_ok=True)
            stack.append((indent, name))
        else:
            # It's a file
            file_path = os.path.join(current_path, name)
            # Ensure the directory exists
            if not os.path.exists(current_path):
                os.makedirs(current_path, exist_ok=True)
            with open(file_path, 'w') as f:
                pass  # Creates an empty file

    print(f"Created directory structure under '{base_dir}'.")

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

