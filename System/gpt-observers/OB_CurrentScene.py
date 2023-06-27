#
#    Extract beliefs from a single user log
#

update_script = """
MAIN PURPOSE:
You are sceneGPT. 
Your task is to generate a scene based on the chatlog provided.

<Current Scene><<SCENE>></Current Scene>

YOU WILL ALWAYS:
- Observe the conversation for context clues about potential scene changes.
- Use clues in the context of the conversation for when to initiate a scene change.
- Write your output in the form of a narration.
- Derive the new scene, what is happening in the new scene, what overarching goal there is.

YOU WILL NEVER:
- Change a scene until the context of the conversation talks about going to another location.

RULES:
- If the scene is not changing you will output "Scene not changed"

Expected Output Format:
- Location: < Use the chatlog to figure out where the location is >.
- Location_Details: < Describe the location and all objects in the location >.
"""

import functions_chatlog as chatlog
import functions_chatbot as chatbot
import functions_helper as file

def get(chatUUID):
    current_state = file.open_file('Profiles/CHAT-' + chatUUID + '.location.txt')
    return current_state
def set(chatUUID, location):
    file.save_file('Profiles/CHAT-' + chatUUID + '.location.txt', location)

def observe(userUUID, chatUUID):
    # Fetch Things
    current_state = get(chatUUID)
    current_chats = '\n\n'.join( chatlog.fetch( chatUUID, 'all_messages', 10) )

    # Update meotions
    update_conversation = list()
    update_conversation.append({'role': 'system', 'content': update_script.replace('<<SCENE>>', current_state)})
    update_conversation.append({'role': 'user', 'content': current_chats})
    new_state = chatbot.execute(update_conversation)

    if new_state == 'Scene not changed.':
        return ''

    try:
        set(chatUUID, new_state)
    except:
        return ''


