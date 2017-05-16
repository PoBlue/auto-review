# -*- coding: utf-8 -*-
"""
hadler for web page
"""
from flask import Flask, request, render_template, redirect, url_for, make_response
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories
from web_handle_func import review_get, review_post, setting_page_get, setting_page_post, has_value, create_review_file
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
        return render_template("new_data.html")
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


if __name__ == '__main__':
    app.debug = True
    app.run()
