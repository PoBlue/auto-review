# -*- coding: utf-8 -*-
"""
hadler for web page
"""
from flask import Flask, request, render_template, redirect, url_for, make_response
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories
from web_handle_func import review_get, review_post, setting_page_get, setting_page_post, has_value, create_review_file
import json
app = Flask(__name__)


@app.route('/review', methods=['GET', 'POST'])
def review():
    """
    review page
    """
    if request.method == 'POST':
        selected_path = request.cookies.get('selected-path')
        return review_post(request.form, selected_path)
    else:
        selected_path = request.args.get('selected_project')
        return review_get(selected_path)


@app.route('/', methods=['GET', 'POST'])
def setting_handle():
    """
    set project dir path
    """
    if request.method == 'POST':
        return setting_page_post(request)
    else:
        return setting_page_get(request)


@app.route('/reset/path')
def reset_project_path():
    """
    reset project path
    """
    resp = make_response(render_template('setdir.html'))
    resp.set_cookie('project-path', expires=0)
    return resp


@app.route('/data', methods=['GET', 'POST'])
def review_data():
    """
    manuplate review data
    """
    all_data_paths = get_filepaths("data/")
    return render_template('data_file_list.html', data_paths=all_data_paths)


@app.route('/data/new', methods=['GET', 'POST'])
def new_data_file():
    """
    create new data file
    """
    if request.method == "GET":
        return render_template("new_data_file.html")
    elif request.method == "POST":
        file_name = request.form["file_name"]
        if has_value(file_name):
            if create_review_file(file_name) is not False:
                return "sucessful"
            else:
                return "falure"
    else:
        return "falure"


@app.route('/data/<data_path>/edit')
def data_edit(data_path):
    """
    edit data in data path
    """
    return data_path


@app.route('/data/<data_path>/add', methods=['GET', 'POST'])
def add_new_data(data_path):
    """
    add new data to file in data_path
    """
    if request.method == 'POST':
        save_review_data(request.form, data_path)
        return "sucessful"
    elif request.method == 'GET':
        return render_template("new_data_review.html", data_path=data_path)
    else:
        return "Error: other method in add_new_data"


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
    new_review_data['id'] = review_id
    return new_review_data


if __name__ == '__main__':
    app.debug = True
    app.run()
