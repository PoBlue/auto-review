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


def save_review_data(form, data_path):
    """
    add a new review data
    """
    file_path = 'data/' + data_path
    review_dict = json_file_to_dict(file_path)
    new_id = create_review_id(review_dict['reviews'])
    new_review_data = parser_data(form, new_id)
    review_dict['reviews'].append(new_review_data)
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
        if data['id'] > 0:
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
    new_review_data['comment'] = form['comment']
    new_review_data['rate'] = form['rate']
    if has_value(form.get('pos_regex')):
        new_review_data['pos_regex'] = form['pos_regex']
    else:
        new_review_data['pos_regex'] = ""
    new_review_data['description'] = form['description']
    new_review_data['id'] = review_id
    return new_review_data