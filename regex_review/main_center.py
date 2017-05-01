from base_func import get_filepaths, parse_file, AllReviewsData

DIR_PATH = "/Users/blues/Desktop/ArcadeGame-4"
REL_FILE_PATHS = get_filepaths(DIR_PATH)

for review_data in AllReviewsData("data/fend_p5.json"):
    print("rate: %s, comment: %s, regex: %s" % (review_data.get_comment(),
                                                review_data.get_rate(),
                                                review_data.get_regex()))

for path in REL_FILE_PATHS:
    LINE_NUMBER = parse_file('/Users/blues/Desktop/test.js', 'return')
    print(path)
    print("line num: %d" % (LINE_NUMBER))
