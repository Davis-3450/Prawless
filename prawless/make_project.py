import os

# Define the directory structure
directory_structure = {
    'reddit_wrapper': {
        'core': {
            '__init__.py': '',
            'base.py': '',
            'exceptions.py': '',
            'paginator.py': '',
            'logging_config.py': ''
        },
        'clients': {
            '__init__.py': '',
            'reddit_client.py': ''
        },
        'entities': {
            '__init__.py': '',
            'submission.py': '',
            'user.py': '',
            'subreddit.py': '',
            'comment.py': ''
        },
        'iterators': {
            '__init__.py': '',
            'user_submission_iterator.py': ''
        },
        'main.py': ''
    }
}

# Define the root directory
root_directory = os.path.abspath('reddit_wrapper')

# Function to create the directory structure
def create_directory_structure(root, structure):
    for item, content in structure.items():
        item_path = os.path.join(root, item)
        if isinstance(content, dict):
            # If content is a dictionary, create a directory and recurse
            if not os.path.exists(item_path):
                os.makedirs(item_path)
            create_directory_structure(item_path, content)
        else:
            # If content is a string, create a file with the content
            with open(item_path, 'w') as f:
                f.write(content)

# Create the directory structure starting from the root directory
create_directory_structure(root_directory, directory_structure)

print("Reddit Wrapper file structure created successfully.")
