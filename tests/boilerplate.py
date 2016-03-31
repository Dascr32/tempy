import os
from random import choice
from string import ascii_uppercase

file_names = ["foo.txt", "testing.txt", "somefile.txt"]
all_entries = ["foo.txt", "testing.txt", "somefile.txt", "dummy"]


def create_testing_dir(dir_path):
    """
    Creates a dir with 3 files, 1 sub directory with 1 file and 1 dir.
    Total entries: 4
    Size: About 48 bytes
    """
    # Create some files in root dir
    for file_name in file_names:
        with open(os.path.join(dir_path, file_name), "w") as new_file:
                new_file.write(''.join(choice(ascii_uppercase) for i in range(12)))

    # Create a dir in root dir
    dummy_dir = os.path.join(dir_path, "dummy")
    os.mkdir(dummy_dir)

    # Create a file in dummy dir
    with open(os.path.join(dummy_dir, "test.txt"), "w") as new_file:
                new_file.write(''.join(choice(ascii_uppercase) for i in range(12)))

    # Create a dir in dummy dir
    os.mkdir(os.path.join(dummy_dir, "subdir"))