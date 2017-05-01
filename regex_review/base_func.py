import re
import os


def parse_file(path, regex):
    """
    get the line number that matched regular expression
    """
    pattern = re.compile(regex, re.MULTILINE)
    with open(path, 'rb') as file:
        data = file.read().decode('utf-8')
        pos = pattern.search(data)
        line_number = data.count('\n', 0, pos.start())
        return line_number


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, directory)
            file_paths.append(rel_path)

    return file_paths

# # --TEST--
# # Run the above function and store its results in a variable.
# rel_file_paths = get_filepaths("/Users/blues/Desktop/ArcadeGame-4")

# for path in rel_file_paths:
#     print(path)

# # test parse file
# ln = parse_file('/Users/blues/Desktop/test.js', 'return')
# print("line num: %d" % (ln))

