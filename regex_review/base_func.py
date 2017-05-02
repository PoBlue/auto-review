"""this module have basic function for pasing file"""
import re
import os
import json


def parse_file(path, regex):
    """
    get the line number that matched regular expression
    """
    pattern = re.compile(regex, re.MULTILINE)
    with open(path, 'rb') as file:
        data = file.read().decode('utf-8')
        pos = pattern.search(data)
        if pos is None:
            return None
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


class AllReviewsData():
    """
    class for storing all reviews data
    """
    def __init__(self, json_file):
        self.current = 0
        with open(json_file, 'r') as file:
            self.data = json.load(file)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.get_length():
            review = self.get_review(self.current)
            self.current += 1
            return review
        else:
            raise StopIteration

    def get_length(self):
        """
        get the length of reviews
        """
        return len(self.get_reviews())

    def get_reviews(self):
        """
        get reviews
        """
        return self.data['reviews']

    def get_review(self, i):
        """
        get review with index
        """
        return ReviewData(self.data['reviews'][i])


class ReviewData():
    """
    class for an review data
    """
    def __init__(self, data):
        self.data = data

    def get_regex(self):
        """
        get regural expression
        """
        return self.data['regex']

    def get_comment(self):
        """
        get review comment
        """
        return self.data['comment']

    def get_rate(self):
        """
        get rete
        """
        return self.data['rate']


class JsReviewData():
    """
    easy for creating review data structure
    """
    def __init__(self):
        self.all_datas = []

    def add_review(self, path, review):
        """
        add review to specify path
        """
        for data in self.all_datas:
            if data['path'] == path:
                data['reviews'].append(review)
                return
        new_data = {}
        new_data['path'] = path
        new_data['reviews'] = [review]
        self.all_datas.append(new_data)

    def to_json(self):
        """
        convert data to json string
        """
        return json.dumps(self.all_datas)


def regex_dir(dir_path, selected_files, data_file):
    """
    parse file and return js review data json
    """
    js_review_data = JsReviewData()
    for review in AllReviewsData(data_file):
        for path in selected_files:
            line_number = parse_file(dir_path + path, review.get_regex())
            if line_number is not None:
                new_review_data = {}
                new_review_data["lineNum"] = line_number
                new_review_data["comment"] = review.get_comment()
                new_review_data["rate"] = review.get_rate()
                js_review_data.add_review(path, new_review_data)
    return js_review_data
# # --TEST--
# # Run the above function and store its results in a variable.
# rel_file_paths = get_filepaths("/Users/blues/Desktop/ArcadeGame-4")

# for path in rel_file_paths:
#     print(path)

# # test parse file
# ln = parse_file('/Users/blues/Desktop/test.js', 'return')
# print("line num: %d" % (ln))
