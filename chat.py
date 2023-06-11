import chromadb
from chromadb.config import Settings
import openai
from time import time, sleep
from uuid import uuid4
import json
import argparse
import sys


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
gpt_persona_directory = 'gpt_personas'
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
def chatbotFetchAction(name):
    content = open_file(gpt_actions_directory + '/' + name + '.txt')
    return content;
def chatbotFetchPersona(name):
    content = open_file(gpt_persona_directory + '/' + name + '.txt')
    return content;


#
# KB management
#   filename - What name to store the database under
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
def KBAdd(filename, chatlog):
    # Fetch Relavant Memories
    collection = KBInit(filename)
    kb, kb_id = KBSearch(filename, chatlog, 1)

    # Prepare script for conversation
    chatbot_update_kb_script = chatbotFetchScript('kb_update')
    chatbot_update_kb_script = chatbot_update_kb_script.replace('<<KB>>', kb)

    # Have conversation with GPT
    kb_conversation = list()
    kb_conversation.append({'role': 'system', 'content': chatbot_update_kb_script})
    kb_conversation.append({'role': 'user', 'content': chatlog})
    updated_memory = chatbot(kb_conversation)

    # If memory is not too long then save
    if len(updated_memory.split(' ')) < 1000:
        collection.update(ids=[kb_id],documents=[updated_memory])
        return updated_memory, kb_id

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
#   chatlog_name - Where to save the chatlog
#   profile - Subcatagory for specifying storage
#
chatLogs = {}
chatLogDirectory = 'chatdb'
def chatInit(chatlog_name, profile):
    profile = chatlog_name + '-' + profile
    filepath = chatLogDirectory + '/' + profile + '.json'
    if profile in chatLogs:
        save_json(filepath, chatLogs[profile])
        return chatLogs[profile]
    
    chatLogs[profile] = open_json(filepath,[])
    return chatLogs[profile]
def chatAdd(chatlog_name, profile, data):
    chatlog = chatInit(chatlog_name, profile)
    chatlog.append(data)
    return chatInit(chatlog_name, profile)
def chatFetch(chatlog_name, profile, entries=3):
    chatlog = chatInit(chatlog_name, profile)
    if (entries==-1):
        return chatlog
    if entries >= len(chatlog):
        return chatlog
    else:
        return chatlog[-entries:]

# Personality Profiles - Profile === human for which you are talking to
userProfileDirectory = 'user_profiles'
def userInit(filename, create_default=False):
    data = open_file(userProfileDirectory + '/' + filename + '.txt')
    if data == '' and create_default == True:
        return open_file(userProfileDirectory + '/_new_profile.txt')
    return data
def userUpdate(filename, new_user_messages):
    # Get Current Profile
    current_profile = userInit(filename)
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
    save_file(userProfileDirectory + '/' + filename + '.txt', new_profile)
    return new_profile

if __name__ == '__main__':
    # instantiate chatbot
    openai.api_key = open_file('key_openai.txt')

    # 
    #   Handle arguments
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-user", help="The profile of the user chatting with the bot. String 'Taylor-Public'.")
    parser.add_argument("-savechat", help="Name of the chatlog to save and continue from. String 'Taylor-AI-Conversation'.")
    parser.add_argument("-savekb", help="KBs to update with new text. String 'Taylor-private'.")
    parser.add_argument("-saveuser", help="User profile to save too. String 'Taylor-private'.")
    parser.add_argument("-knownusers", help="Profiles that the AI knows about. Comma-seprated string 'Taylor-private,Taylor-public'.")
    parser.add_argument("-knownkbs", help="Knowledge bases to pull information from. Comma-seprated string 'kbone,kbtwo,kbthree'.")
    parser.add_argument("-action", help="Action to use be taken from gpt_actions directory. Default 'default_chat'.")
    parser.add_argument("-lang", help="Language that the bot should use. Default 'English'.")
    parser.add_argument("-persona", help="How the bot should behave based on script in gpt_personas. Default 'Louis_Theroux'.")
    parser.add_argument("-topic", help="Set a topic to talk about. Default is 'No Topic Selected'.")
    parser.add_argument("-say", help="What to say to the bot.. Hello bot! Nice to meet you!")
    args = parser.parse_args()

    current_user = args.user
    save_chat = args.savechat
    save_kb = args.savekb
    save_profile = args.saveuser
    known_profiles = args.knownusers.split(',')
    known_kb = args.knownkbs.split(',')
    conversation_topic = args.topic
    conversation_language = args.lang
    chatbot_persona = args.persona
    chatbot_action = args.action
    text = current_user + ":" + args.say

    # 
    #   Save Chat Logs
    #
    chatAdd(save_chat, 'user_messages', text) # Add user message to personal log
    chatAdd(save_chat, 'all_messages', 'USER: %s' % text) # Add user message to merged conversation log
    chatAdd(save_chat, 'conversation', {'role': 'user', 'content': text}) # Add user message as JSON object to conversation


    # 
    #   Search Long Term memory and pull relavant memories
    #
    search_term = chatFetch(save_chat, 'all_messages', 5) # Get the log of current conversation
    search_term = '\n\n'.join(search_term).strip() # Convert into a string
    kb = list()
    for kb_name in known_kb:
        kb_text, kb_id = KBSearch(kb_name, search_term, 1)
        if kb_text != "No new KB article could be created based on the given chat logs.":
            kb.append( '<memory>' + kb_text + '</memory>' ) # Fetch One Relavant conversation from the database

    #
    #   Fetch other_profiles
    #
    other_profiles = list()
    for profile_name in known_profiles:
        profile_text = userInit(profile_name)
        if profile_text != '':
            other_profiles.append('<person>' + userInit(profile_name) + '</person>')


    #
    #   Load the script for GPT, Insert the arguments needed
    #
    user_profile = '<person>' + userInit(current_user, True) + '</person>'
    chatbot_persona_script = chatbotFetchPersona(chatbot_persona)
    chatbot_process_script = chatbotFetchAction(chatbot_action)
    chatbot_process_script = chatbot_process_script.replace('<<PERSONA>>', chatbot_persona_script) # Add user profile into instructions
    chatbot_process_script = chatbot_process_script.replace('<<PROFILE>>', user_profile) # Add user profile into instructions
    chatbot_process_script = chatbot_process_script.replace('<<KB>>', ''.join(kb)) # Add long-term memory into instructions
    chatbot_process_script = chatbot_process_script.replace('<<FRIEND_PROFILES>>', ''.join(other_profiles)) # Add user profile into instructions
    chatbot_process_script = chatbot_process_script.replace('<<TOPIC>>', ''.join(conversation_topic)) # Add user profile into instructions
    chatbot_process_script = chatbot_process_script.replace('<<LANG>>', ''.join(conversation_language)) # Add user profile into instructions
    chatbot_process_script = chatbot_process_script.replace('\n',' ').replace('  ',' ')
    
    #
    #   Execute conversation and recieve output
    #
    current_conversation = chatFetch(save_chat,'conversation',-1) # Pull entire conversation JSONS
    current_conversation[0]['content'] = chatbot_process_script # Update last message content

    response = chatbot(current_conversation) # Fetch response
    print('\n\nCHATBOT: %s' % response) # Output


    # 
    #   Save all the details of the covnersation
    #
    print('\n\nSaving things...')
    chatAdd(save_chat,'conversation', {'role': 'assistant', 'content': response}) # Update conversation with assistant's dialog
    chatAdd(save_chat,'all_messages','CHATBOT: %s' % response) # add to general log

    latest_user_outputs = '\n'.join(chatFetch(save_chat,'user_messages',3)).strip()
    userUpdate(save_profile, latest_user_outputs) # Update user profile with latest notes

    # TODO: Label each KB with the context (user & date)
    lastest_conversation = '\n\n'.join(chatFetch(save_chat,'all_messages', 5)).strip()
    KBAdd(save_kb, lastest_conversation) # Update longterm Memory with lastest conversation

    # Write Chroma Database
    chroma_client.persist()
