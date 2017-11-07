# -*- coding: utf-8 -*-
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

    def get_description(self):
        """
        get the description of regex
        """
        return self.data['description']

    def is_match(self):
        """
        need to be match?
        """
        return self.data['isMatch']


class JsReviewData():
    """
    easy for manuplating review data structure
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

    def group_review_by_line_num(self):
        """
        group review if it's line is same
        """
        for path_data in self.all_datas:
            grouped_data = group_item_by_key(path_data['reviews'], "lineNum")
            combined_data = combine_review_in_same_key(grouped_data)
            path_data['reviews'] = combined_data
        print(self.all_datas)


def group_item_by_key(datas, key):
    """
    return a dict that is grouped
    """
    grouped_data = {}
    for item in datas:
        grouped_data.setdefault(item[key], []).append(item)
    return grouped_data


def combine_review_in_same_key(datas):
    """
    combine review in same key
    return:
        array that is in same key
    """
    combined_reviews = []
    for key, reviews in datas.items():
        new_review = combine_reviews(reviews)
        combined_reviews.append(new_review)
    return combined_reviews


def combine_reviews(reviews):
    """
    combine review in same line
    """
    new_review = reviews[0]
    combined_comment = new_review['comment']
    combined_desc = new_review['description']
    results = combine_comment_and_desc(reviews)
    if results is not None:
        combined_comment, combined_desc = results
    new_review['comment'] = combined_comment
    new_review['description'] = combined_desc
    rate = suggestion_rate(reviews)
    if rate is not None:
        new_review['rate'] = rate
    return new_review


def combine_comment_and_desc(reviews):
    """
    produce a new review
    """
    comment_template = "# 建议 %s ✨ %s \n---------\n %s \n"
    description_template = "%s %s: %s\n"
    reviews_len = len(reviews)
    if reviews_len <= 1:
        return None

    combined_comment = ""
    combined_desc = ""
    for i in range(0, reviews_len):
        review_data = reviews[i]
        marker = get_marker(review_data['rate'])
        if i == 0:
            combined_comment = comment_template % (i + 1,
                                                   marker,
                                                   review_data['comment'])
            combined_desc = description_template % (i + 1,
                                                    marker,
                                                    review_data['description'])
        else:
            combined_comment += comment_template % (i + 1,
                                                    marker,
                                                    review_data['comment'])
            combined_desc += description_template % (i + 1,
                                                     marker,
                                                     review_data['description'])
    return (combined_comment, combined_desc)


def suggestion_rate(reviews):
    """
    return the suggestion rate for the grouped review
    """
    for review_data in reviews:
        rate = review_data['rate']
        if rate == "require":
            return rate
    return None


def get_marker(rate):
    """
    return a marker for review
    """
    if rate == "awesome":
        return "(做得不错的点)"
    elif rate == "suggestion":
        return ""
    elif rate == "require":
        return "(下面这一点需要修改才能通过项目)"


def generate_review_data(line_num, review):
    """
    generate review data to result file
    """
    new_review_data = {}
    new_review_data["lineNum"] = line_num
    new_review_data["comment"] = review.get_comment()
    new_review_data["rate"] = review.get_rate()
    new_review_data["description"] = review.get_description()
    return new_review_data


def regex_dir(dir_path, selected_files, data_file):
    """
    parse file and return js review data json
    """
    js_review_data = JsReviewData()
    for review in AllReviewsData(data_file):
        # pass if condition is not satisfied
        if not condiction_check(review):
            continue
        for path in selected_files:
            file_path = dir_path + path
            new_review_data = generate_js_review_data(file_path,
                                                      review,
                                                      review.get_regex())
            if new_review_data is not None:
                if review.get_is_missed() is not True:
                    js_review_data.add_review(path, new_review_data)
                    break
            else:
                if review.get_pos_regex() != "":
                    regex = review.get_pos_regex()
                    new_review_data = generate_js_review_data(file_path,
                                                              review,
                                                              regex)
                    if new_review_data is not None:
                        js_review_data.add_review(path, new_review_data)
                        break
    return js_review_data


def condiction_check(review):
    """
    check if review pass condcitons
    """
    is_match = False #check if review need to match
    if review.is_match():
        is_match = True
    else:
        is_match = False
    return is_match


def generate_js_review_data(file_path, review, regex):
    """
    generate js review data
    """
    line_number = parse_file(file_path, regex)
    if line_number is not None:
        return generate_review_data(line_number,
                                    review)
    return None


# # --TEST--
# # Run the above function and store its results in a variable.
# rel_file_paths = get_filepaths("/Users/blues/Desktop/ArcadeGame-4")

# for path in rel_file_paths:
#     print(path)

# # test parse file
# ln = parse_file('/Users/blues/Desktop/test.js', 'return')
# print("line num: %d" % (ln))
