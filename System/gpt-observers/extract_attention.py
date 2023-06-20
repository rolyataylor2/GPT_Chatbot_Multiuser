#
#    Extract beliefs from a single user log
#

update_script = """
MAIN PURPOSE:
You are attentionGPT. You are an expert in analyzing conversational logs to identify the main topics or subjects that a person is paying attention to.

Your task is to analyze and extract the key areas of focus for the USER based on their recent chats.

The USER input will be a list of their most recent conversations.

EXTRACTION OF ATTENTION:
Your output should represent the main topics or subjects that the USER is paying attention to, without including any additional information.

RULES:
- Extract the topics or subjects the USER is focusing on, excluding any irrelevant details.
- Do not include any other observations in your output.
- Your output should consist of words or phrases that represent the main areas of attention.
- Be concise and clear in your extraction.
- Avoid duplicating or overlapping topics in your output.
- Your output should be a comma seperated list
"""
import functions_chatlog as chatlog
import functions_chatbot as chatbot
import functions_helper as file
import functions_profile as profile
import time, json
def Get(userUUID):
    current_state = profile.get(userUUID + '.atten')
    try:
        json.loads(current_state)
    except:
        current_state = {}
        current_state['last_update'] = int(time.time())
        current_state['attentions'] = {}
    return current_state

def Set(userUUID, data):
    try:
        profile.set(userUUID + '.atten', json.dumps(data))
        return True
    except:
        return False
    
def Analyse(userUUID, chatUUID):
    # Collect things
    current_state = Get(userUUID)
    current_chat = chatlog.fetch( chatUUID, 'user_' + userUUID, 5)

    # Reduce attention by number of seconds elapsed
    seconds_elapsed = int(time.time()) / 60
    for value, key in current_state['attention']:
        current_state['attention'][key] -= seconds_elapsed
        if current_state['attention'][key] < 0:
            current_state['attention'][key] = 0
    current_state['last_update'] = int(time.time())

    # Figure out some more attention items
    conversation = list()
    conversation.append({'role': 'system', 'content': update_script})
    conversation.append({'role': 'user', 'content': current_chat})
    try:
        update_state = ','.split( chatbot.execute(conversation) )
    except:
        update_state = []

    # Add 10 minutes to each attention item
    for key in update_state:
        if current_state['attention'].get(key) is not None:
            current_state['attention'][key] += 10*60*60
        else:
            current_state['attention'][key] = 10*60*60

    # Save this...
    Set(userUUID, current_state)
    return current_state

