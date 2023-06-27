import os
import shutil

def delete_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

def delete_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)

def delete_files_without_persona(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and "persona" not in file:
            os.remove(file_path)

# Delete files in the ./Chatlog directory
chatlog_directory = "./Chatlogs"
delete_files_in_directory(chatlog_directory)

# Delete files in the ./KnowledgeBase directory
knowledgebase_directory = "./KnowledgeBase"
delete_files_in_directory(knowledgebase_directory)

# Delete folders in the ./Chatlog directory
delete_folders(chatlog_directory)

# Delete folders in the ./KnowledgeBase directory
delete_folders(knowledgebase_directory)

# Delete files in the ./Profiles directory that don't contain "persona" in their filename
profiles_directory = "./Profiles"
delete_files_without_persona(profiles_directory)
