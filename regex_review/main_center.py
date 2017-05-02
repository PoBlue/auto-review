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


class Parser(object):
    """
    parse file and then create file that chrome can excute
    """
    def __init__(self, project_path):
        self.selected_file_paths = []
        self.review_data_path = ""
        self.review_project_path = ""
        self.project_path = project_path
        self.chorme_path = "chrome-extension/auto_review/"
        self.src_files_js = ["src_files/tool.js",
                             "src_files/review_functions.js",
                             "src_files/main.js"]

    def set_review_args(self, selected_paths, review_project_path,
                        review_data_path):
        """
        set selected paths
        """
        self.selected_file_paths = selected_paths
        self.review_project_path = review_project_path
        self.review_data_path = review_data_path

    def creat_chorme_excfile(self):
        """
        combine data and file into result file that chrome
        extension will inject into page
        """
        data_code = "var DATA = %s;\n"
        result_path = self.project_path + self.chorme_path + 'result.js'
        with open(result_path, 'w') as outfile:
            outfile.write(data_code % (regex_dir(self.review_project_path,
                                                 self.selected_file_paths,
                                                 self.review_data_path)
                                       .to_json()))
            for fname in self.src_files_js:
                with open(self.project_path + fname) as infile:
                    for line in infile:
                        outfile.write(line)

parser = Parser(PROJECT_PATH)
parser.set_review_args(SELECTED_FILE_PATHS, DIR_PATH, DATA_FILE)
parser.creat_chorme_excfile()

# creat_chorme_excfile()
print(regex_dir(DIR_PATH, SELECTED_FILE_PATHS, DATA_FILE).to_json())
