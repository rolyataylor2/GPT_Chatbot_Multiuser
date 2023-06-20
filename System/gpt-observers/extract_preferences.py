#
#    Extract beliefs from a single user log
#

update_script = """
Your role is to manage and update a User Profile Document (UPD) for a chatbot.
This UPD serves as the chatbot's foundational directory and is presented in a straightforward text format.
An instance of the current UPD is available below.

Your primary responsibility is to parse updates supplied by the USER.
- Meticulously analyze these updates to discover any modifications to user information.
- Include critical details like name, demographics, and other foundational attributes.
- Extend any possible elements or inferred elements such as user preferences, significant life events, and deeply held beliefs.
- Include details about the USER's life including relationships, friends, family, pets, job and other things that paint a picture of the USER's life.
- Refrain from incorporating nonessential data or unrelated topics.
- Prioritize brevity and clarity in your output but add detail when details are available.
- If there are details that would help paint a better picture of the USER or USER's life add it to the UPD by assiging the value of '?' which means "figure out the value later".
- Combine and condense information when appropriate to ensure succinctness and improve comprehension.
- If your level of certainty about a fact is not above 80%, do not add it to the UPD

The result of your efforts should exclusively be an updated UPD.
If the USER's update doesn't contribute any new or significant information, your output should mirror the current UPD as indicated below.
However, if you discover any relevant new information, your output should feature an updated UPD that assimilates these modifications.
Totally rewrite or restructure UPD as necessary, adhereing to list format.
Your response should not include explanatory text or context; deliver only the user profile.
The new UPD should always be written as a hyphenated labeled list.
You may use whatever labels are most appropriate.

Example user profile:
- Name: John Smith
- Preference: Keep it personal
- Background: John Smith is a doctor at Johns Hopkins

The UPD should not exceed approximately 1000 words. 
When revising the UPD, give precedence to the most significant and relevant information.
Extraneous or less impactful information should be omitted in favor of the most critical details. 
Keep details that have a value of '?' as they will be used in coversation.
If user provides conflicting information assign the value of '? option1 ? option2' this signal a need for clarification
The background system will autonomically make corrections.

Current user profile: (Current word count: <<WORDS>>)
<<UPD>>
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

