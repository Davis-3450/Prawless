import os

def print_directory_structure(startpath):
    """
    Print the directory structure of the directory provided in startpath.
    """
    for root, dirs, files in os.walk(startpath):
        # Determine the depth of the current directory
        level = root.replace(startpath, '').count(os.sep)
        
        # Indent the current directory
        indent = ' ' * 4 * level
        
        # Print the current directory
        print(f'{indent}{os.path.basename(root)}/')
        
        # Indent the filenames under the current directory
        sub_indent = ' ' * 4 * (level + 1)
        
        for f in files:
            print(f'{sub_indent}{f}')

# Use the script
if __name__ == "__main__":
    # Use the current working directory as the starting point
    directory_path = os.getcwd()
    print_directory_structure(directory_path)
