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
description += '    ' + GREEN + 'Action:' + RESET + ' Continues Conversation in the Chatroom\n'
description += '        Saves $dialog to the $chatUUID under the identity of $userUUID\n'
description += '        Adds Memories, Updates Profiles, and Updates Personas\n\n'
description += '    ' + GREEN + 'Ideas:' + RESET + '\n'
description += '        - Use $savekbs to Create a Public Profile for the $userUUID to be shared.\n'
description += '        - Use $savepersona to mix personas by an unrelated persona.\n'
description += '        - Use $savekbs to create a public KB that contains expertise skills: "Carpenter-Skills-Public"\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)

# Required arguments
parser.add_argument("-userUUID", metavar=' ', help='User-UUID', required=True)
parser.add_argument("-chatUUID", metavar=' ', help='Chatroom-UUID', required=True, default='general')
parser.add_argument("-dialog", metavar=' ', required=True, help="Dialog to save to the chat")
parser.add_argument("-apikey", metavar=' ', required=True, help="Your OpenAI API key.\n" + RED + "CAUTION:" + RESET + " $$$\n ")


# Optional arguments
parser.add_argument("-savekbs", metavar=' ', required=False, default='', help="Merge Into Additional KBs:\n" + GREEN + "Type:" + RESET + " Comma-Delimited-List\n" + GREEN + "Always updates:" + RESET + " $chatUUID,$userUUID\n ")
parser.add_argument("-savepersona", metavar=' ', required=False, default='', help="Merge Additional Personas\n" + GREEN + "Type:" + RESET + " Comma-Delimited-List\n" + GREEN + "Always updates:" + RESET + " $userUUID\n ")
parser.add_argument("-saveprofile", metavar=' ', required=False, default='', help="Merge Additional Profiles\n" + GREEN + "Type:" + RESET + " Comma-Delimited-List\n" + GREEN + "Always updates:" + RESET + " $userUUID\n ")

parser.add_argument("-freezekb", metavar=' ', required=False, default='N', help="Dont write personal KBs")
parser.add_argument("-freezepersona", metavar=' ', required=False, default='N', help="Dont write personal persona")
parser.add_argument("-freezeprofile", metavar=' ', required=False, default='N', help="Dont write personal profile")

args = parser.parse_args()
# @TODO create flags for not saving default persona, profile, kb

#
#   Imports
#
import chromadb
from chromadb.config import Settings
import openai
from time import time, sleep
from uuid import uuid4
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
  
#
# GPT handler
#
gpt_scripts_directory = 'gpt_scripts'
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
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = messages.pop(1)
                print('\n\n DEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)
def chatbotFetchScript(name):
    content = open_file(gpt_scripts_directory + '/' + name + '.txt')
    return content;

#
#   KB management
#
knowledgeBasesDirectory = 'chromadb'
chroma_client = chromadb.Client(Settings(persist_directory=knowledgeBasesDirectory,chroma_db_impl="duckdb+parquet",))
def kbInit(kb_name):
    return chroma_client.get_or_create_collection(name=kb_name)
def kbSearch(kb_name, context, limit_results=1):
    # Fetch the right collection
    collection = kbInit(kb_name)
    if collection.count() == 0:
        return "No KB articles yet", -1

    # Search Database, return results
    results = collection.query(query_texts=[context], n_results=limit_results)
    kb = results['documents'][0][0]
    kb_id = results['ids'][0][0]
    return kb, kb_id
def kbAdd(kb_name, chatlog):
    # Fetch Relavant Memories
    collection = kbInit(kb_name)
    kb, kb_id = kbSearch(kb_name, chatlog, 1)

    # Prepare script for conversation
    kb_conversation = list()
    chatbot_update_kb_script = chatbotFetchScript('kb_update')
    chatbot_update_kb_script = chatbot_update_kb_script.replace('<<KB>>', kb)
    kb_conversation.append({'role': 'system', 'content': chatbot_update_kb_script})
    kb_conversation.append({'role': 'user', 'content': chatlog})
    updated_memory = chatbot(kb_conversation)

    # If memory is not too long then save
    if len(updated_memory.split(' ')) < 1000:
        if collection.count() == 0:
            kb_id = str(uuid4())
            collection.add(ids=[kb_id],documents=[updated_memory])
        else:
            collection.update(ids=[kb_id],documents=[updated_memory])
        return updated_memory, kb_id
    return kbSplit(updated_memory, collection, kb_id)
def kbSplit(updated_memory, collection, kb_id):
    # Prepare script for splitting
    chatbot_split_kb_script = chatbotFetchScript('kb_split')

    # Have Conversation with GPT
    kb_conversation = list()
    kb_conversation.append({'role': 'system', 'content': chatbot_split_kb_script })
    kb_conversation.append({'role': 'user', 'content': updated_memory})
    memories = chatbot(kb_conversation)

    # Split the results
    memories = memories.split('ARTICLE 2:')

    # Update first memory
    memories[0] = memories[0].replace('ARTICLE 1:', '').strip()
    collection.update(ids=[kb_id],documents=[memories[0]])

    # Create new memory
    new_id = str(uuid4())
    memories[1] = memories[1].strip()
    collection.add(documents=[memories[1]],ids=[new_id])

    # Log output: save_file('db_logs/log_%s_split.txt' % time(), 'Split document %s, added %s:\n%s\n\n%s' % (kb_id, new_id, a1, a2))
    return memories[1], new_id

#
# Chatlog management
#
chatLogs = {}
chatLogDirectory = 'chatdb'
def chatSync(chatlog_name, catagory):
    # Store under catagory
    profile = chatlog_name + '-' + catagory
    filepath = chatLogDirectory + '/' + profile + '.json'

    # If loaded then save, if not loaded then load
    if profile in chatLogs:
        save_json(filepath, chatLogs[profile])
    else:
        chatLogs[profile] = open_json(filepath,[])
    
    # Return the log
    return chatLogs[profile]
def chatFetch(chatlog_name, catagory, entries=3):
    # Load
    chatlog = chatSync(chatlog_name, catagory)
    # Splice
    if (entries==-1):
        return chatlog
    if entries >= len(chatlog):
        return chatlog
    else:
        return chatlog[-entries:]
def chatAdd(chatlog_name, catagory, data):
    # Load
    chatlog = chatSync(chatlog_name, catagory)
    # Append
    chatlog.append(data)
    # Save
    return chatSync(chatlog_name, catagory)

#
#   Manage Profiles
#
userProfileDirectory = 'gpt_profiles'
def userInit(profile_name, create_default=False):
    data = open_file(userProfileDirectory + '/' + profile_name + '.txt')
    if data == '' and create_default == True:
        return open_file(userProfileDirectory + '/_new_profile.txt')
    return data
def userAdd(profile_name, new_user_messages):
    # Get Current Profile
    current_profile = userInit(profile_name)
    profile_length = len(current_profile.split(' '))

    # Prepare script for conversation
    chatbot_update_profile_script = chatbotFetchScript('uprofile_update')
    chatbot_update_profile_script = chatbot_update_profile_script.replace('<<UPD>>', current_profile)
    chatbot_update_profile_script = chatbot_update_profile_script.replace('<<WORDS>>', str(profile_length))
    
    # Have conversation with gpt
    profile_conversation = list()
    profile_conversation.append({'role': 'system', 'content': chatbot_update_profile_script})
    profile_conversation.append({'role': 'user', 'content': new_user_messages})
    new_profile = chatbot(profile_conversation)

    # Save updated profile
    save_file(userProfileDirectory + '/' + profile_name + '.txt', new_profile)
    return new_profile

#
#   Manage Personas
#
userPersonaDirectory = 'gpt_personas'
def personaInit(persona_name):
    data = open_file(userPersonaDirectory + '/' + persona_name + '.txt')
    if data == '':
        return open_file(userPersonaDirectory + '/_new_persona.txt')
    return data
def personaAdd(persona_name, conversation, analyseUUID):
    # Get Current Profile
    current_persona = personaInit(persona_name)
    persona_length = len(current_persona.split(' '))

    # Prepare script for conversation
    chatbot_update_persona_script = chatbotFetchScript('persona_update')
    chatbot_update_persona_script = chatbot_update_persona_script.replace('<<UPD>>', current_persona)
    chatbot_update_persona_script = chatbot_update_persona_script.replace('<<WORDS>>', str(persona_length))
    chatbot_update_persona_script = chatbot_update_persona_script.replace('<<UUID>>', analyseUUID)

    # Have conversation with gpt
    persona_conversation = list()
    persona_conversation.append({'role': 'system', 'content': chatbot_update_persona_script})
    persona_conversation.append({'role': 'user', 'content': conversation})
    new_persona = chatbot(persona_conversation)

    # Save updated persona
    save_file(userPersonaDirectory + '/' + persona_name + '.txt', new_persona)
    return new_persona

if __name__ == '__main__':
    # instantiate chatbot
    openai.api_key = args.apikey

    # UUID of user and bot, bots are treated as users
    current_user = args.userUUID
    save_chat = args.chatUUID

    # Save memories ot kbs
    save_kbs = args.savekbs.split(',')
    if args.savekbs == '':
        save_kbs = []
    if args.freezekb == 'N':
        save_kbs.append(current_user)
        save_kbs.append(save_chat)

    # Update Profiles
    save_profiles = args.saveprofile.split(',')
    if args.saveprofile == '':
        save_profiles = []
    if args.freezeprofile == 'N':
        save_profiles.append(current_user)

    # Upate Personas
    save_personas = args.savepersona.split(',')
    if args.savepersona == '':
        save_personas = []
    if args.freezepersona == 'N':
        save_personas.append(current_user)

    # 
    #   Save Chat Logs
    #
    text = args.dialog
    chatAdd(save_chat, 'user_' + current_user, text) # Add user message to personal log
    chatAdd(save_chat, 'all_messages', current_user + ': ' + text) # Add user message to merged conversation log
    chatAdd(save_chat, 'conversation', {'role': 'user', 'content': current_user + ': ' + text}) # Add user message as JSON object to conversation

    #
    #   Update profiles
    #
    latest_user_outputs = '\n\n'.join( chatFetch( save_chat, 'user_' + current_user, 3)).strip()
    for profile in save_profiles:
        userAdd(profile, latest_user_outputs) # Update user profile with latest notes
    
    #
    #   Update Persona
    #
    latest_conversation = '\n\n'.join( chatFetch( save_chat, 'all_messages', 5)).strip()
    for persona in save_personas:
        personaAdd(persona, latest_conversation, current_user)

    # 
    #   Update KBs
    #
    latest_conversation = '\n\n'.join( chatFetch( save_chat, 'all_messages', 5)).strip()
    for kb in save_kbs:
        kbAdd(kb, latest_conversation)

    # Write Chroma Database
    chroma_client.persist()
