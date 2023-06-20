#
#    Extract beliefs from a single user log
#

update_script = """
MAIN PURPOSE:
You are emotionalGPT. You are an expert in emotional psychology when expressed via text messages and conversations.

Your task is to analyze and compile emotional states of the USER who is talking that represents how the USER is feeling those emotions using only emoji.

The USER input will be a list of their most recent chats.

EMOTIONAL STATES
Happy, Sad, Excited, Anxious, Angry, Content, Frustrated, Surprised, Bored, Enthusiastic, Nervous, Grateful, Jealous, Confident, Hopeful, Disappointed, Curious, Embarrassed, Guilty, Lonely, Proud, Irritated, Overwhelmed, Relieved, Impatient, Indifferent, Sympathetic, Insecure, Motivated, Reflective, Sick, Nauseous, Fever, Pain. Grateful, irritable, cranky, upset, tired, irrational.

RULES
- Do not include any information besides the USER's emotional state.
- Do not include events, objects, locations or people.
- Your output will be a series of emoji that describe how the user is feeling. Be creative in using multiple emoji to express complex emotions. Include all emotional states, not just the ones listed above.
- Use multiple emoji to emphasize an emotion.
- Your output will not contain words, numbers or letters, only emoji.
- Your output will be no longer than 10 emoji.
"""
import functions_chatlog as chatlog
import functions_chatbot as chatbot
import functions_helper as file
def Get(userUUID):
    current_state = file.open_file('gpt_profiles/' + userUUID + '.emote.txt')
    return current_state
def Analyse(userUUID, chatUUID):
    # Fetch Things
    current_state = Get(userUUID)
    userOnlyChats = chatlog.fetch( chatUUID, 'user_' + userUUID, 5)

    # Update meotions
    update_conversation = list()
    update_conversation.append({'role': 'system', 'content': update_script})
    update_conversation.append({'role': 'user', 'content': userOnlyChats})
    new_state = chatbot.execute(update_conversation)

    current_state = Get(userUUID) + new_state[:10]
    file.save_file('gpt_profiles/' + userUUID + '.emote.txt', current_state[-100:])
    return current_state

