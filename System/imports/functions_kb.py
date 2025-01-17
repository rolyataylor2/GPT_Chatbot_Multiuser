#
#   Imports
#
import functions_chatbot as chatbot
import os
import functions_helper as file
knowledgeBasesDirectory = 'KnowledgeBase'


#
#  Update the directory indexes
#
def update_directory(kb_name):
    # Directory path
    kb_dir = knowledgeBasesDirectory + '/' + kb_name + '/'
    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir)
    
    # Compile a list of files and keywords
    directory = ''
    for filename in os.listdir(kb_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(kb_dir, filename)
            try:
                kb = file.open_json(filepath)
                directory += '\n%s - %s - %s - %s\n' % (filename, kb['title'], kb['description'], kb['keywords'])
            except:
                print('KB article is an invalid JSON file:')
                print('    filename:' + filepath)
                continue
    
    file.save_file(kb_dir + '_dir.txt', directory.strip())

#
# Create things
#
def create_body(text):
    system = chatbot.getScript('FS_KB_Create_Body')
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': text})
    return chatbot.execute(messages)
def create_keywords(text):
    system = chatbot.getScript('FS_KB_Create_Keywords')
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': text})
    return chatbot.execute(messages)

import re
def create_title(text):
    system = chatbot.getScript('FS_KB_Create_Title')
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': text})
    return re.sub(r'[^a-zA-Z0-9]', '', chatbot.execute(messages)[:30])
def create_description(text):
    system = chatbot.getScript('FS_KB_Create_Description')
    
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': text})
    return chatbot.execute(messages)
def create(text):
    article = {}
    article['body'] = create_body(text)
    article['title'] = create_title(article['body'])
    article['keywords'] = create_keywords(article['body'])
    article['description'] = create_description(article['body'])
    return article

#
# Merge body text or articles
#
def merge_body(body_one, body_two):
    system = chatbot.getScript('FS_KB_Merge_Body')
    system.replace('<<KB>>', body_one)
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': body_two})
    return chatbot.execute(messages)
def merge(article, article2):
    new_article = {}
    new_article['body'] = merge_body(article['body'], article2['body'])
    new_article['title'] = article['title']
    new_article['keywords'] = create_keywords(article['body'])
    new_article['description'] = create_description(new_article['body'])
    return new_article

#
# Update/Add KB directory
#
def update(kb_names, text):
    # Create a memory
    memory = create(text)
    hybrid_memory = ''

    # Save to kbs
    for kb in kb_names:
        # Directory path
        directory = knowledgeBasesDirectory + '/' + kb + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Search the KB
        file_list = search(kb, text)['Sorted_Filenames']

        # No memory found, so save this one
        if len(file_list) == 0:
            file.save_json(directory + memory['title'] + '.json', memory)
            update_directory(kb)
            continue
       
        # Merge new memory with old memory
        article = file.open_json(directory + file_list[0])
        if article == {}:
            file.save_json(directory + memory['title'] + '.json', memory)
        else:
            hybrid_memory = merge(article, memory)
            file.save_json(directory + file_list[0], hybrid_memory)
        
#
# Search KB directory for articles
#
import yaml
def parse_yaml(yaml_string):
    try:
        parsed_object = yaml.safe_load(yaml_string)
        return parsed_object
    except yaml.YAMLError as e:
        print("Error parsing YAML:", e)
        return None
def search(kb_name, query):
    # Directory path
    directory = knowledgeBasesDirectory + '/' + kb_name + '/'
    if not os.path.exists(directory):
        return {'Sorted_Filenames':[], 'concat':''}
    
    # Append files
    directory_index = file.open_file(directory + '/_dir.txt')
    system = chatbot.getScript('FS_KB_Search_Dir').replace('<<DIRECTORY>>', directory_index)
    
    # Push chat
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': query})
    response = chatbot.execute(messages)
    
    # Check output
    try:
        response = parse_yaml(response)
        return response
    except:
        return {'Sorted_Filenames':[], 'concat':''}
