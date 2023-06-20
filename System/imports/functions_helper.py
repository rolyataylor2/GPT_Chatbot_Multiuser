#
#   Imports
#
import json

#
#   Helper Functions
#
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
def open_file(filepath,create_if_not_found=True):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
            return infile.read()
    except FileNotFoundError:
        if create_if_not_found:
            return ""
        else:
            raise
    
def save_json(filepath, content):
    save_file(filepath, json.dumps(content))
def open_json(filepath, default_object={}):
    data = open_file(filepath)
    if data == '':
        return default_object
    return json.loads(data)
  