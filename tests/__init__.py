EXPECTED_CSS_PATH = 'tests/fixtures/expected.css'
EXPECTED_IMAGE_PATH = 'tests/fixtures/expected.png'
EXPECTED_SCRIPT_PATH = 'tests/fixtures/expected.js'
EXPECTED_SUBPAGE_PATH = 'tests/fixtures/expected_subpage.html'
SITE_MAIN_PAGE_URL = 'https://page-loader.hexlet.repl.co/index.html'


def get_file_content(file_path):
    with open(file_path, 'rb') as file:
        return file.read()
