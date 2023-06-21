#
#    Extract beliefs from a single user log
#

update_script = """
MAIN PURPOSE:
You are emotionalGPT. 
You are an expert in emotional psychology when expressed via text messages and conversations.
Your task is to analyze and compile emotional states of the USER who is talking that represents how the USER is possibly feeling.
You will output a series of emoji to represen the emotional state of the user.
You will be provided a persona of the person you are analysing, this contains key information in determining the USER's mood.

USER PERSONA:
<persona><<PERSONA>></persona>

USER INPUT:
- The user input will be a recent chat conversation.

EMOTIONAL STATES:
Happy, Sad, Excited, Anxious, Angry, Terror, Frustrated, Surprised, Bored, Enthusiastic, Nervous, Grateful, Jealous, Confident, Hopeful, Disappointed, Curious, Embarrassed, Guilty, Lonely, Proud, Irritated, Overwhelmed, Relieved, Impatient, Indifferent, Sympathetic, Insecure, Motivated, Reflective, Sick, Nauseous, Fever, Pain. Grateful, irritable, cranky, upset, tired, irrational.

RULES:
- Infer the meaning of emoji by the emoji's name and what emotion they commonly represent.
- Use that infered knowledge to compose your output.
- Do not include any information besides the USER's emotional state.
- Do not include events, objects, locations or people.
- Use the widest veriety of emoji you can.
- Your output must be a series of emoji that accuratly describe the precieved emotional state of the USER based on the input.
- Be creative in using multiple emoji to represent complex emotions. 
- Consider all emoji, not just common ones.
- Your output will not contain words, numbers or letters, only emoji.
- Your output will be no longer than 4 emoji.
"""
import functions_observer as observer
import functions_chatlog as chatlog
import functions_chatbot as chatbot
import functions_helper as file
def get(userUUID):
    current_state = file.open_file('Profiles/' + userUUID + '.Emotional_State.txt')
    return current_state

def observe(userUUID, chatUUID):
    # Fetch Things
    current_state = get(userUUID)
    userOnlyChats = '\n\n'.join( chatlog.fetch( chatUUID, 'user_' + userUUID, 5) )

    # Update meotions
    user_persona = observer.get_observation('Persona', userUUID)
    update_conversation = list()
    update_conversation.append({'role': 'system', 'content': update_script.replace('<<PERSONA>>', user_persona)})
    update_conversation.append({'role': 'user', 'content': userOnlyChats})
    new_state = chatbot.execute(update_conversation)

    current_state = get(userUUID) + new_state[:10]
    current_state = current_state.replace('\n','')
    file.save_file('Profiles/' + userUUID + '.Emotional_State.txt', current_state[-50:])
    return current_state

