# -*- coding: utf-8 -*-
"""
hadler for web page
"""
from flask import Flask, request, render_template, redirect, url_for, make_response
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories
from web_handle_func import review_get, review_post, setting_page_get, setting_page_post, has_value, create_review_file, save_review_data, json_file_to_dict, remove_review_data, save_review_to_file
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


@app.route('/data/<data_path>/<int:review_id>/edit', methods=['GET', 'POST'])
def data_edit(data_path, review_id):
    """
    edit data in data path
    """
    if request.method == "POST":
        review_dict = remove_review_data(data_path, review_id)
        save_review_data(request.form, data_path, review_dict, review_id=review_id)
        return redirect(url_for('data_list', data_path=data_path))
    elif request.method == "GET":
        return data_edit_page_get(data_path, review_id)
    else:
        return 'Error in data_edit function: no method matched'


def data_edit_page_get(data_path, review_id):
    """
    handle get method from data edit page
    """
    reviews = json_file_to_dict('data/' + data_path)['reviews']
    founded_review_data = {}
    for review_d in reviews:
        if review_d['id'] == review_id:
            founded_review_data = review_d
    return render_template('data_review_edit.html',
                           data_path=data_path,
                           review=founded_review_data)


@app.route('/data/<data_path>/<int:review_id>/remove')
def data_remove(data_path, review_id):
    """
    remove review data in data path according review id
    """
    review_dict = remove_review_data(data_path, review_id)
    save_review_to_file(data_path, review_dict)
    return redirect(url_for('data_list', data_path=data_path))


@app.route('/data/<data_path>/list')
def data_list(data_path):
    """
    edit data in data path
    """
    all_reviews = json_file_to_dict('data/' + data_path)['reviews']
    return render_template('data_review_list.html',
                           data_path=data_path,
                           all_reviews=all_reviews)


@app.route('/data/<data_path>/add', methods=['GET', 'POST'])
def add_new_data(data_path):
    """
    add new data to file in data_path
    """
    if request.method == 'POST':
        file_path = 'data/' + data_path
        review_dict = json_file_to_dict(file_path)
        save_review_data(request.form, data_path, review_dict)
        return "sucessful"
    elif request.method == 'GET':
        return render_template("new_data_review.html", data_path=data_path)
    else:
        return "Error: other method in add_new_data"


if __name__ == '__main__':
    app.debug = True
    app.run()
