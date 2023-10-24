import os

def generate_tree(directory, prefix=""):
    """
    Generate a directory tree representation for the specified directory.
    
    :param directory: The root directory to generate the tree for.
    :param prefix: The current prefix (used for recursion).
    :return: A string representation of the directory tree.
    """
    tree = prefix + '├── ' + os.path.basename(directory) + '/\n'
    if os.path.isdir(directory):
        items = [item for item in os.listdir(directory) if item != '__pycache__']
        
        # If the directory is `.git`, print it as a single entity and skip processing its children.
        if os.path.basename(directory) == '.git':
            return tree
        
        for index, item in enumerate(sorted(items)):
            item_path = os.path.join(directory, item)
            if index == len(items) - 1:
                # Last item, so adjust the prefix accordingly
                tree += generate_tree(item_path, prefix + '    ')
            else:
                tree += generate_tree(item_path, prefix + '│   ')
    
    return tree

# Test
directory_path = "/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/"
print(generate_tree(directory_path))
