from base_func import get_filepaths, parse_file

# --TEST--
# Run the above function and store its results in a variable.
rel_file_paths = get_filepaths("/Users/blues/Desktop/ArcadeGame-4")

for path in rel_file_paths:
    print(path)

# test parse file
LINE_NUMBER = parse_file('/Users/blues/Desktop/test.js', 'return')
print("line num: %d" % (LINE_NUMBER))
