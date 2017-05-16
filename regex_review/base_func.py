"""this module have basic function for pasing file"""
import re
import os
import json


def get_immediate_subdirectories(a_dir):
    """
    all of the immediate subdirectories
    """
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


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

    def get_default_num(self):
        """
        get default line number
        """
        return self.data['default_num']

    def get_is_missed(self):
        """
        we can check if we should add review depend on the state
        """
        return self.data['is_missed']

    def get_pos_regex(self):
        """
        get the position that match regex to review
        """
        return self.data['pos_regex']


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


def generate_review_data(line_num, comment, rate):
    """
    generate review data to result file
    """
    new_review_data = {}
    new_review_data["lineNum"] = line_num
    new_review_data["comment"] = comment
    new_review_data["rate"] = rate
    return new_review_data


def regex_dir(dir_path, selected_files, data_file):
    """
    parse file and return js review data json
    """
    js_review_data = JsReviewData()
    for review in AllReviewsData(data_file):
        for path in selected_files:
            file_path = dir_path + path
            new_review_data = generate_js_review_data(file_path,
                                                      review,
                                                      review.get_regex())
            if new_review_data is not None:
                if review.get_is_missed() is not True:
                    js_review_data.add_review(path, new_review_data)
            else:
                if review.get_pos_regex() != "":
                    regex = review.get_pos_regex()
                    new_review_data = generate_js_review_data(file_path,
                                                              review,
                                                              regex)
                    if new_review_data is not None:
                        js_review_data.add_review(path, new_review_data)
    return js_review_data


def generate_js_review_data(file_path, review, regex):
    """
    generate js review data
    """
    line_number = parse_file(file_path, regex)
    if line_number is not None:
        return generate_review_data(line_number,
                                    review.get_comment(),
                                    review.get_rate())
    return None


# # --TEST--
# # Run the above function and store its results in a variable.
# rel_file_paths = get_filepaths("/Users/blues/Desktop/ArcadeGame-4")

# for path in rel_file_paths:
#     print(path)

# # test parse file
# ln = parse_file('/Users/blues/Desktop/test.js', 'return')
# print("line num: %d" % (ln))
