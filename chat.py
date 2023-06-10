import chromadb
from chromadb.config import Settings
import openai
import yaml
from time import time, sleep
from uuid import uuid4

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()
    
# GPT handler
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

# KB management - Profile === database with which to work with
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
        kb_conversation = list()
        kb_conversation.append({'role': 'system', 'content': chatbotFetchScript('kb_init')})
        kb_conversation.append({'role': 'user', 'content': 'Hello'})
        article = chatbot(kb_conversation)
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

# Chatlog management - profile === Username of the person you are talking with
chatLogs = {}
# TODO: save to files and load from files
def chatInit(username, profile):
    profile = username + '-' + profile
    if profile in chatLogs:
        return chatLogs[profile]
    
    chatLogs[profile] = list()
    return chatLogs[profile]
def chatAdd(username, profile, data):
    chatlog = chatInit(username, profile)
    chatlog.append(data)
    return 0
def chatFetch(username, profile, entries=3):
    chatlog = chatInit(username, profile)
    if (entries==-1):
        return chatlog
    if entries >= len(chatlog):
        return chatlog
    else:
        return chatlog[-entries:]

# Personality Profiles - Profile === human for which you are talking to
userNotes = {}
userNotesDirectory = 'user_profiles'
def userInit(filename):
    return open_file(userNotesDirectory + '/' + filename + '.txt')
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
    save_file(userNotesDirectory + '/' + filename + '.txt', new_profile)
    return new_profile

if __name__ == '__main__':
    # instantiate chatbot
    openai.api_key = open_file('key_openai.txt')

    # Arguments
    #   --user = Username of the person who is making the inquiry
    #   --save-chat = Names of chat logs
    #   --save-kb = KBs that this conversation should be saved too
    #   --known-users = Profiles the AI can access
    #   --known-kb = KBs the AI can search
    #   --action = chat, event, code, something
    #   --lang = language to use
    #   --persona = personality of the chatbot
    #   --topic = topic of conversation
    #   
    #   This_Script.py
    #   --user=Taylor 
    #   --save-chat=AI_Taylor_Private 
    #   --save-kb=AI_Taylor_Private
    #   --save-profile=Taylor_Private
    #   --known-profiles=Taylor_Private,Taylor_Public,Jack_Public,Thomas_Public,Tiki_Public
    #   --known-kb=AI_Taylor_Private,AI_Taylor_Public,AI_Jack_Public,AI_Thomas_public,AI_Tiki_Public
    #   --lang=english
    #   --AI-Personality=92834283
    #   "What is jack's favorite food?"
    #
    current_user = "Rolyataylor2"
    save_chat = "AI_Rolyataylor2_Private"
    save_kb = "Rolyataylor2_Private"
    save_profile = "Rolyataylor2_Private"
    known_profiles = "Taylor_Private,Taylor_Public,Jack_Public,Thomas_Public,Tiki_Public".split(',')
    known_kb = "AI_Taylor_Private,AI_Taylor_Public,AI_Jack_Public,AI_Thomas_public,AI_Tiki_Public".split(',')
    language = "english"
    ai_personality = "southern-bell"
    conversation_topic = 'ethics'
    text = '\n\nHello my name is ' + current_user

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
    
    # TODO: search all databases in known_kb variable
    kb = list()
    for i in known_kb:
        kb.append( KBSearch(known_kb[i], search_term, 1) ) # Fetch One Relavant conversation from the database


    #
    #   Load the script for GPT, Insert the arguments needed
    #
    user_profile = userInit(save_profile)
    chatbot_process_script = chatbotFetchScript('chatbot_process')
    chatbot_process_script = chatbot_process_script.replace('<<PROFILE>>', user_profile) # Add user profile into instructions
    chatbot_process_script = chatbot_process_script.replace('<<KB>>', ''.join(kb)) # Add long-term memory into instructions

    # @TODO Load profiles from known_profiles so the bot knows about the people in the conversation
    
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

    lastest_conversation = '\n\n'.join(chatFetch(save_chat,'all_messages', 5)).strip()
    KBAdd(save_kb, lastest_conversation) # Update longterm Memory with lastest conversation

    # Write Chroma Database
    chroma_client.persist()
