"""
this module store the funciton that handle the page get or post method
"""
from flask import Flask, request, render_template, redirect, url_for, make_response
from main_center import Parser
from base_func import get_filepaths, get_immediate_subdirectories


def has_value(value):
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