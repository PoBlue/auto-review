# -*- coding: utf-8 -*-
"""
hadler for web page
"""
from flask import Flask, request, render_template, redirect, url_for, make_response
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories
app = Flask(__name__)


@app.route('/review', methods=['GET', 'POST'])
def review():
    """
    handle request from web
    """
    if request.method == 'POST':
        selected_path = request.cookies.get('selected-path')
        return handle_post(request.form, selected_path)
    else:
        selected_path = request.args.get('selected_project')
        return handle_get(selected_path)


@app.route('/', methods=['GET', 'POST'])
def setting_handle():
    """
    set project dir path
    """
    if request.method == 'POST':
        selected_project_path = request.form["select-project-path"]
        project_dir = request.cookies.get('project-path')
        selected_path = project_dir + '/' + selected_project_path + '/'
        return redirect(url_for('review', selected_project=selected_path))
    else:
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
    return render_template('review_data.html')


def has_value(value):
    return value != "" and value is not None


def handle_post(form, selected_path):
    """
    handle post method
    """
    parser = Parser()
    parser.set_review_args(form.getlist("file-paths"),
                           selected_path,
                           form["data-path"])
    parser.creat_chorme_excfile()
    return "sucessful"


def handle_get(selected_path):
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

if __name__ == '__main__':
    app.debug = True
    app.run()
