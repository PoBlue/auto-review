"""this is the main logic to parse file and ui controler"""
from base_func import get_filepaths, regex_dir

DIR_PATH = "/Users/blues/Desktop/ArcadeGame-4/"
DATA_FILE = "data/fend_p5.json"
REL_FILE_PATHS = get_filepaths(DIR_PATH)

SELECTED_FILE_PATHS = ["js/app.js", "js/engine.js"]
PROJECT_PATH = "/Users/blues/Desktop/auto-review/"
CHORME_PATH = "chrome-extension/auto_review/"

FILENAMES = ["src_files/tool.js",
             "src_files/review_functions.js",
             "src_files/main.js"]

DATA_CODE = "var DATA = %s;\n"


def creat_chorme_excfile():
    with open(PROJECT_PATH + CHORME_PATH + 'result.js', 'w') as outfile:
        outfile.write(DATA_CODE % (regex_dir(DIR_PATH,
                                             SELECTED_FILE_PATHS,
                                             DATA_FILE).to_json()))
        for fname in FILENAMES:
            with open(PROJECT_PATH + fname) as infile:
                for line in infile:
                    outfile.write(line)

creat_chorme_excfile()
print(regex_dir(DIR_PATH, SELECTED_FILE_PATHS, DATA_FILE).to_json())
