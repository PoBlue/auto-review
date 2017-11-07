"""
this module store the funciton that handle the page get or post method
"""
from flask import Flask, request, render_template, redirect, url_for, make_response
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories
import json


def has_value(value):
    """
    check if value is empty value or None
    """
    return value != "" and value is not None


def review_post(form, selected_path):
    """
    handle post method
    """
    parser = Parser()
    parser.set_review_args(form.getlist("file-paths"),
                           selected_path,
                           form["data-path"])
    parser.creat_chorme_excfile()
    return "sucessful"


def review_get(selected_path):
    """
    handle get method
    """
    all_file_paths = get_filepaths(selected_path)
    all_data_paths = get_filepaths("data/")
    resp = make_response(render_template("index.html",
                                         file_paths=all_file_paths,
                                         data_paths=all_data_paths))
    resp.set_cookie('selected-path', selected_path)
    return resp


def setting_page_post(request):
    """
    handle post method from setting page
    """
    selected_project_path = request.form["select-project-path"]
    project_dir = request.cookies.get('project-path')
    selected_path = project_dir + '/' + selected_project_path + '/'
    return redirect(url_for('review', selected_project=selected_path))


def setting_page_get(request):
    """
    handle get method from setting page
    """
    project_dir = request.args.get('project-path')
    if not has_value(project_dir):
        project_dir = request.cookies.get('project-path')
    if has_value(project_dir):
        all_project_paths = get_immediate_subdirectories(project_dir + "/")
        resp = make_response(render_template('select.html',
                                             project_paths=all_project_paths))
        resp.set_cookie('project-path', project_dir)
        return resp
    else:
        return render_template('setdir.html')


def has_file(path, file_name):
    """
    check if path has file
    """
    all_file_name = get_filepaths(path)
    for name in all_file_name:
        if name == file_name:
            return True
    return False


def create_review_file(name):
    """
    create review file with data
    return:
        - False: can not create file
        - True: create file sucessfully
    """
    data = """{"reviews":[]}"""
    file_name = name + ".json"
    data_path = "data/"
    file_path = data_path + file_name
    if has_file(data_path, file_name):
        return False

    with open(file_path, "w") as data_file:
        data_file.write(data)
    return True


def save_review_data(form, data_path, review_dict, review_id=None):
    """
    add a new review data
    """
    if review_id is None:
        new_id = create_review_id(review_dict['reviews'])
    else:
        new_id = review_id
    new_review_data = parser_data(form, new_id)
    review_dict['reviews'].append(new_review_data)
    save_review_to_file(data_path, review_dict)


def save_review_to_file(data_path, review_dict):
    """
    save review to file
    """
    file_path = 'data/' + data_path
    json_str = json.dumps(review_dict)
    with open(file_path, 'w') as review_f:
        review_f.write(json_str)


def create_review_id(all_reviews):
    """
    create a id for data
    """
    if not all_reviews:
        return 0

    largest_id = 0
    for data in all_reviews:
        if data['id'] > largest_id:
            largest_id = data['id']
    return largest_id + 1


def json_file_to_dict(path):
    """
    paser a josn file to dict
    """
    with open(path, 'r') as review_file:
        return json.load(review_file)


def parser_data(form, review_id):
    """
    parser data from form
    """
    new_review_data = {}
    new_review_data['regex'] = form['regex']
    if has_value(form.get('is_missed')):
        new_review_data['is_missed'] = True
    else:
        new_review_data['is_missed'] = False

    # isMatched key set
    if has_value(form.get('is_matched')):
        new_review_data['isMatch'] = True
    else:
        new_review_data['isMatch'] = False

    new_review_data['comment'] = form['comment']
    new_review_data['rate'] = form['rate']
    if has_value(form.get('pos_regex')):
        new_review_data['pos_regex'] = form['pos_regex']
    else:
        new_review_data['pos_regex'] = ""
    new_review_data['description'] = form['description']
    new_review_data['id'] = review_id
    return new_review_data


def remove_review_data(data_path, review_id):
    """
    return a new review dict that specify id is removed
    """
    file_path = 'data/' + data_path
    review_dict = json_file_to_dict(file_path)
    remove_index = 0
    for review_d in review_dict['reviews']:
        if review_d['id'] == review_id:
            review_dict['reviews'].remove(review_dict['reviews'][remove_index])
            break
        remove_index += 1
    return review_dict


def get_review_with_id(data_path, review_id):
    """
    get a review with id and data_path
    """
    reviews = get_reviews_with_data_path(data_path)
    founded_review_data = {}
    for review_d in reviews:
        if review_d['id'] == review_id:
            founded_review_data = review_d
    return founded_review_data


def get_reviews_with_data_path(data_path):
    """
    get all reviews in data_path
    """
    all_reviews = json_file_to_dict('data/' + data_path)['reviews']
    return all_reviews


def create_review_id_in_data_path(data_path):
    """
    create an review id in a data path
    """
    all_reviews = get_reviews_with_data_path(data_path)
    return create_review_id(all_reviews)


def copy_review_to_file(from_path, to_path, review_id):
    """
    copy an review to a file
    """
    founded_review = get_review_with_id(from_path, review_id)
    selected_path_reviews = get_reviews_with_data_path(to_path)
    new_review_id = create_review_id_in_data_path(to_path)
    founded_review['id'] = new_review_id
    selected_path_reviews.append(founded_review)
    review_dict = {'reviews': selected_path_reviews}
    save_review_to_file(to_path, review_dict)
