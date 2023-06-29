#
#   Imports
#
import functions_helper as file
chatLogDirectory = 'ChatLogs'

#
#   Handle Chatlogs
#
def load(chatlog_name, catagory):
    profile = chatlog_name + '-' + catagory
    filepath = chatLogDirectory + '/' + profile + '.json'
    return file.open_json(filepath,[])
def save(chatlog_name, catagory, whole_chatlog):
    profile = chatlog_name + '-' + catagory
    filepath = chatLogDirectory + '/' + profile + '.json'
    file.save_json(filepath, whole_chatlog)
    return
def fetch(chatlog_name, catagory, entries=3):
    # Load
    chatlog = load(chatlog_name, catagory)
    # Splice
    if (entries==-1):
        return chatlog
    if entries >= len(chatlog):
        return chatlog
    else:
        return chatlog[-entries:]
    
from datetime import datetime


def add(chatlog_name, catagory, data):
    # Load
    chatlog = fetch(chatlog_name, catagory, -1)
    # Append
    current_time = datetime.now().strftime("%I:%M%p")
    chatlog.append( f"[{current_time}] {data}" )
    # Save
    save(chatlog_name, catagory, chatlog)
    return chatlog

