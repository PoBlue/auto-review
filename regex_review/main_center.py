"""this is the main logic to parse file and ui controler"""
from base_func import get_filepaths, regex_dir

DIR_PATH = "/Users/blues/Desktop/ArcadeGame-4/"
DATA_FILE = "data/fend_p5.json"
REL_FILE_PATHS = get_filepaths(DIR_PATH)

SELECTED_FILE_PATHS = ["js/app.js", "js/engine.js"]

print(regex_dir(DIR_PATH, SELECTED_FILE_PATHS, DATA_FILE).to_json())
