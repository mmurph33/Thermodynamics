import os

def list_files(startpath):
    ignore_items = ['.DS_Store', '__pycache__', '.git']
    for root, dirs, files in os.walk(startpath):
        # Remove ignored directories from the list so they won't be traversed
        dirs[:] = [d for d in dirs if d not in ignore_items]
        
        # Calculate the depth level of the current directory
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        
        # Print the directory name
        print('{}{}/'.format(indent, os.path.basename(root)))
        
        # Calculate the sub-indentation for the files
        subindent = ' ' * 4 * (level + 1)
        
        # Print the files in the directory
        for f in files:
            if f not in ignore_items:
                print('{}{}'.format(subindent, f))

# Set your start path
start_path = '.'  # Current directory
list_files(start_path)
