# -*- coding: utf-8 -*-
"""
hadler for web page
"""
from flask import Flask, request, render_template
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories
app = Flask(__name__)


@app.route('/review', methods=['GET', 'POST'])
def request_handle():
    """
    handle request from web
    """
    if request.method == 'POST':
        return handle_post(request.form)
    else:
        return handle_get()


@app.route('/', methods=['GET', 'POST'])
def setting_handle():
    """
    set project dir path
    """
    project_dir = request.args.get('project-path')
    if project_dir != "" and project_dir is not None:
        all_project_paths = get_immediate_subdirectories(project_dir + "/")
        return render_template('select.html', project_paths=all_project_paths)
    else:
        return render_template('setdir.html')


def handle_post(form):
    """
    handle post method
    """
    test_dir_path = "/Users/blues/Desktop/ArcadeGame-4/"
    parser = Parser()
    parser.set_review_args(form.getlist("file-paths"),
                           test_dir_path,
                           form["data-path"])
    parser.creat_chorme_excfile()
    return "sucessful"


def handle_get():
    """
    handle get method
    """
    test_dir_path = "/Users/blues/Desktop/ArcadeGame-4/"
    all_file_paths = get_filepaths(test_dir_path)
    all_data_paths = get_filepaths("data/")
    return render_template("index.html", file_paths=all_file_paths,
                           data_paths=all_data_paths)

if __name__ == '__main__':
    app.debug = True
    app.run()
