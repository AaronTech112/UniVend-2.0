import os
import sys

# Get the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))

# Define media directory and subdirectories
media_dir = os.path.join(project_dir, 'media')
subdirs = [
    'listing_images',
    'profile_pics',
    'message_images',
    'student_ids'
]

# Create media directory if it doesn't exist
if not os.path.exists(media_dir):
    try:
        os.makedirs(media_dir)
        print(f"Created media directory: {media_dir}")
    except Exception as e:
        print(f"Error creating media directory: {e}")
        sys.exit(1)
else:
    print(f"Media directory already exists: {media_dir}")

# Create subdirectories
for subdir in subdirs:
    subdir_path = os.path.join(media_dir, subdir)
    if not os.path.exists(subdir_path):
        try:
            os.makedirs(subdir_path)
            print(f"Created subdirectory: {subdir_path}")
        except Exception as e:
            print(f"Error creating subdirectory {subdir_path}: {e}")
    else:
        print(f"Subdirectory already exists: {subdir_path}")

print("Media directories setup completed.")