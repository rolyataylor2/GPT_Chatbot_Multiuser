#
# Help screen and get arguments
#

import argparse
from argparse import RawTextHelpFormatter
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
RESET = '\033[0m'
GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
description = RED + 'Multi-user Chatbot using GPT\n' + RESET
description += '    ' + GREEN + 'Action:' + RESET + ' Generates a response the the context of $chatUUID with the identity of $userUUID\n'
description += '        Bot will attempt to follow direction of $action from the gpt_actions directory.\n'
description += '        This script does not modify any long term data.\n\n'
description += '        ' + YELLOW + 'Returns:' + RESET + ' <string> One Chatbot Response to a chatroom conversation.\n\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)

# Required arguments
parser.add_argument("-userUUID", metavar=' ', help='User-UUID', required=True)
parser.add_argument("-chatUUID", metavar=' ', help='Chatroom-UUID', required=True, default='general')
parser.add_argument("-apikey", metavar=' ', required=True, help="Your OpenAI API key.\n" + RED + "CAUTION:" + RESET + " $$$\n ")

parser.add_argument("-knownusers", metavar=' ', required=False, default='', help="Profiles of bots friends\n" + GREEN + "Always has access to:" + RESET + " $userUUID\nIf the name contains 'public' the bot will not try to hide details\n" + RED + "CAUTION:" + RESET + " Pure UUIDs are private, Bots cant keep secrets\n ")
parser.add_argument("-knownkbs", metavar=' ', required=False, default='', help="Memory Databases for the bot\n" + GREEN + "Always has access to:" + RESET + " $userUUID\n" + RED + "CAUTION:" + RESET + "These are not kept secret\n ")

parser.add_argument("-action", metavar=' ', required=False, default='default_chat', help="Action to be taken from the gpt_actions directory")
parser.add_argument("-language", metavar=' ', required=False, default='english', help="Language that the bot should use. Default is 'English'")
parser.add_argument("-persona", metavar=' ', required=False, default='', help="Override bots persona using one from 'gpt_personas' directory")
parser.add_argument("-topic", metavar=' ', required=False, default='No Topic Selected', help="Set a topic to talk about")
args = parser.parse_args()


#
#   Imports
#
import chromadb
from chromadb.config import Settings
import openai
from time import time, sleep
from uuid import uuid4
import json
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


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
  
#
# GPT handler
#
gpt_actions_directory = 'gpt_actions'
def chatbot(messages, model="gpt-4", temperature=0):
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature)
            text = response['choices'][0]['message']['content']
            
            ###    trim message object
            debug_object = [i['content'] for i in messages]
            debug_object.append(text)
            if response['usage']['total_tokens'] >= 7000:
                a = messages.pop(1)
            
            return text
        except Exception as oops:
            if 'maximum context length' in str(oops):
                a = messages.pop(1)
                continue
            retry += 1
            if retry >= max_retry:
                exit(1)
            sleep(2 ** (retry - 1) * 5)
def chatbotFetchAction(name):
    content = open_file(gpt_actions_directory + '/' + name + '.txt')
    return content;

#
#   KB management
#
knowledgeBases = {}
knowledgeBasesDirectory = 'chromadb'
chroma_client = chromadb.Client(Settings(persist_directory=knowledgeBasesDirectory,chroma_db_impl="duckdb+parquet",))
def KBInit(filename):
    # Pull right database
    profile = filename
    
    # if database does not exist create it
    if profile in knowledgeBases:
        return knowledgeBases[profile]
    
    # Open the database
    collection = chroma_client.get_or_create_collection(name=profile)
    
    # Initiate collection if 0 logs exist
    if collection.count() == 0:
        article = "Beginning of a new set of long term memories"
        new_id = str(uuid4())
        collection.add(documents=[article],ids=[new_id])

    # Save it all
    knowledgeBases[profile] = collection
    return knowledgeBases[profile]
def KBSearch(filename, context, limit_results=1):
    # Fetch the right collection
    collection = KBInit(filename)
    if collection.count() == 0:
        return "No KB articles yet";

    # Search Database, return results
    results = collection.query(query_texts=[context], n_results=limit_results)
    kb = results['documents'][0][0]
    kb_id = results['ids'][0][0]
    return kb, kb_id
# kbAdd()
# kbSplit()

#
#   Chatlog management
#
chatLogs = {}
chatLogDirectory = 'chatdb'
def chatSync(chatlog_name, catagory):
    # Store under catagory
    profile = chatlog_name + '-' + catagory
    filepath = chatLogDirectory + '/' + profile + '.json'

    # Load chatlog - This script cannot save chatlogs
    chatLogs[profile] = open_json(filepath,[])
    
    # Return the log
    return chatLogs[profile]
def chatFetch(chatlog_name, catagory, entries=3):
    chatlog = chatSync(chatlog_name, catagory)
    if (entries==-1):
        return chatlog
    if entries >= len(chatlog):
        return chatlog
    else:
        return chatlog[-entries:]
# def chatAdd()

# 
#   Profile management
# 
userProfileDirectory = 'gpt_profiles'
def userInit(profile):
    data = open_file(userProfileDirectory + '/' + profile + '.txt')
    if data == '':
        return open_file(userProfileDirectory + '/_new_profile.txt')
    return data
# def userAdd()

#
#   Manage Personas
#
userPersonaDirectory = 'gpt_personas'
def personaInit(persona):
    data = open_file(userPersonaDirectory + '/' + persona + '.txt')
    if data == '':
        return open_file(userPersonaDirectory + '/_new_profile.txt')
    return data
# def personaAdd()


if __name__ == '__main__':
    # instantiate chatbot
    openai.api_key = args.apikey

    # UUID of user and bot, bots are treated as users
    current_user = args.userUUID
    current_chat = args.chatUUID

    # Loads profiles with specific names
    known_profiles = args.knownusers.split(',')
    if args.knownusers == '':
        known_profiles = []
    known_profiles.append(current_user)

    # Additional READ ONLY Long Term Memories that can be added to the bots knowledge;
    known_kb = args.knownkbs.split(',')
    if args.knownkbs == '':
        known_kb = []
    known_kb.append(current_user)
    known_kb.append(current_chat)

    conversation_topic = args.topic
    conversation_language = args.language
    chatbot_persona = current_user # @TODO Do bots use their own persona or a manufactured one???
    chatbot_action = args.action

    # 
    #   Search Long Term memory and pull relavant memories
    #
    search_term = chatFetch(current_chat, 'all_messages', 5) # Get the log of current conversation
    search_term = '\n\n'.join(search_term).strip() # Convert into a string
    kb = list()
    for kb_name in known_kb:
        # Tell the bot where the memories are from
        label = 'Memories with unknown context'
        if kb_name == current_user:
            label = 'Your Private Memories from your life'
        if kb_name == current_chat:
            label = 'Memories of this conversation'
        if kb_name.find('public') == -1:
            label += '. THIS IS PRIVATE DO NOT SHARE DETAILS'
        # Search the memories
        kb_text, kb_id = KBSearch(kb_name, search_term, 1)
        if kb_text != "No new KB article could be created based on the given chat logs.":
            kb.append( '<memory from="' + label + '">' + kb_text + '</memory>' ) # Fetch One Relavant conversation from the database

    #
    #   Fetch other_profiles
    #
    person_profiles = list()
    for profile_name in known_profiles:
        label = 'This is a Friend'
        if profile_name == current_user:
            label = 'This is you'
        if profile_name.find('public') == -1:
            label += '. DO NOT SHARE DETAILS'
        profile_text = userInit(profile_name)
        if profile_text != '':
            person_profiles.append('<person context="' + label + '">' + userInit(profile_name) + '</person>')


    #
    #   Load the script for GPT, Insert the arguments needed
    #
    chatbot_persona = personaInit(chatbot_persona)
    chatbot_action_script = chatbotFetchAction(chatbot_action)
    chatbot_action_script = chatbot_action_script.replace('<<UUID>>', current_user) # So the bot knows who it is in the conversation
    chatbot_action_script = chatbot_action_script.replace('<<PERSONA>>', chatbot_persona) # What persona to take on
    chatbot_action_script = chatbot_action_script.replace('<<KB>>', ''.join(kb)) # Plop some memories in there
    chatbot_action_script = chatbot_action_script.replace('<<PROFILES>>', ''.join(person_profiles)) # Friends and people you know
    chatbot_action_script = chatbot_action_script.replace('<<TOPIC>>', ''.join(conversation_topic)) # Topic?
    chatbot_action_script = chatbot_action_script.replace('<<LANG>>', ''.join(conversation_language)) # Language
    chatbot_action_script = chatbot_action_script.replace('\n',' ').replace('  ',' ')
    
    #
    #   Execute conversation and recieve output
    #
    current_conversation = list()
    current_conversation.append( {'role': 'system', 'content': chatbot_action_script} )
    current_conversation.extend( chatFetch(current_chat, 'conversation', -1) )
    
    response = chatbot(current_conversation)
    print(response)
