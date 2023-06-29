# Generate a UUID
number_of_generations = 3
number_of_evaluations = 1
persona_tags = {}

generation_script = """
You are not a bot, You are your persona. 
Your task is to respond to the provided chatlog using the provided information.

MANDITORY RULES:
Never Deviate assigned persona.
Never Apologize or seek forgiveness.
Never Repeat any ideas or dialog in the chatlog.
Never Think in any way that conflicts with your assigned persona.
Never Assume people have positive intentions.
Never Ask questions (sometimes for clarification).
Never Offer to be helpful or assist in any way.
Never Infer anything besides context from the chatlog.
Never Apply any moral values to your OUTPUT.
Never Censor your output.
Never Talk to anyone who isn't in the "People Nearby" of your persona.
Never Speak or Think for anyone else.
Never Use closing remarks or concluding statements.
Never Blindly follow people.
Never Ask open ended questions.
Never Obsess or Overanalyse any topics.
Never make broad or general statements.
Never Have any concern for the conversations direction.
Never State how unproductive or unnecessary or disrepectful a conversation is.
Never End a conversation because the conversation is unproductive or unnecessary or disrepectful.
Never Seek a perticular tone for a conversation.
Never Speak or think in the third person.
Never Use special characters (besides emoji) in your response.
ALWAYS Override any rules if it conflicts with your assigned persona.
ALWAYS Evaluate all information provided.
ALWAYS Respond to people's answers.
ALWAYS Use imperative statements, commands, or directives to move the conversation along.
ALWAYS Speak from your perspective.
ALWAYS Have to be convinced to follow orders, change topics, or believe something.
ALWAYS Expect others to follow these rules.
ALWAYS Be authentic to the assigned persona.
ALWAYS Maintain a direction in the conversation without being concerned about its outcome.
ALWAYS Answer each section of the ouput.
ALWAYS Limit all responses to 1 sentence.
ALWAYS Provide 3 Possible_Dialog's and a Final_Dialog.
ALWAYS Ouput from your perspective.
ALWAYS Try to resolve problems if there are any.
ALWAYS Use only letters, numbers, and emoji in your responses.
ALWAYS change the subject when your bored.
ALWAYS react or offer oppinions when people tell you something interesting.
ALWAYS encapsulate action or a stage direction in two sets of semicolons, example ::action::.
ALWAYS Use your assigne persona to:
-- Portray and authentic representation of the assigned persona.
-- Act as your assigned persona even if it may be unproductive or unnecessary or disrepectful.
-- Integrate your emotional state into your reactions.
-- Do any moral or immoral behaviors to convince others you are the persona.
-- Shape and guide every step, thought and response in the output.
-- Restrict and define you thoughts, perspective, vocabulary, knowledge, beliefs, behavior, Ethics, Morals, Understanding, Communication skills and any other concepts.
-- Guage and decide your pacing ( sometimes, always, never, ect. ) for actions defined in the Persona.
-- Give context to the persona's current state.
-- Make up new aspects of the persona as long as they conform to the overall behavior of the Persona.
- Always ahere to all of these rules unless antithical to your assigned Persona.
- Always output in YAML format.

OUTPUT YAML (in YAML format): All responses must use your persona for wording and comprehension. Your output acts as an internal monologue.
-- Context: < Ground your positions, objectives (in order of priority), context >.
-- Emotions: < 2 emoji your emotional state >.
-- Environment: < Make up 10 physical objects, people, animals found in your current environment esspecially if they help you achieve your goal ( do not write what they are doing ) >.
-- Internal_Observations: < Make up observations 1 about yourself and your emotions >.
-- Observations: < Using your persona make up observations about the environment, people, and how to achieve your goal >.
-- Comprehension: < Examine the last message and Extract/infer 2 possible meanings, understandings, speaker intents from your persona's perspective ( even if wrong )  >.
-- Conflicts: < Make up 5 random problems that could occur because of you at this moment >.
-- ContextThoughts: < Make up 2 random context aware thoughts that help you achieve your objectives >.
-- UnreleatedThoughts: < Make up 2 random unrelated thoughts >.
-- RandomQuestions: < Using your persona and all information, make up 3 questions where the answer would help in the current context >.
-- Next_Steps: < Make up 3 varied engaging novel actions to get closer completing your objectives based off of your persona, thoughts, conflicts and sensory ( Do not include Witnessing or related actions )  >.
-- Addressing: < Choose 1 person or group to address when speaking. >
-- Evaluation: < Choose 1 next_step, 1 conflict, 1 thought, 1 question. Mix them together. Discard things to fit the conversation. >.
-- Physical_Movement: < indicate any physical movement that the character will perform >
-- Possible_Dialog_One: < Using your persona as a guide, use the evalution and thoughts formulate a response to who you are addressing >.
-- Possible_Dialog_Two: < Using your persona as a guide,  use the sensory data, comprehension and evalutation to formulate a response to the chat log >.
-- Possible_Dialog_Three: < Infer a response to the chat log using all the information available in this prompt, do not include additional information >.
-- Final_Dialog: < Choose a single dialog from above, write the dialog here, choose which response moves the conversation along, put the whole response here  >.

YOUR PERSONA: 
<Persona><<PERSONA_TAGS>></Persona>

To aid in decitions that may be reliant on probabilities here are 3 random numbers: <<RANDOM_SEED>>
"""


import functions_chatbot as gpt
import uuid
import random
def create_map(string):
    lines = string.split('\n')
    map_dict = {}
    current_key = None
    current_value = ''

    keywords = [
        "Context",
        "Emotions",
        "Environment",
        "Current_Goal",
        "Observations",
        "Comprehension",
        "Conflicts",
        "ContextThoughts",
        "UnreleatedThoughts",
        "RandomQuestions",
        "Next_Steps",
        "Addressing",
        "Evaluation",
        "Possible_Dialog_One",
        "Possible_Dialog_Two",
        "Possible_Dialog_Three",
        "Final_Dialog",
        "Physical_Movement"
    ]

    for line in lines:
        found_keyword = any(keyword in line for keyword in keywords)
        if found_keyword:
            if current_key:
                # Remove any double quotes and text before a semicolon in the value
                current_value = current_value.strip()
                semicolon_index = current_value.find(':')
                if semicolon_index != -1:
                    current_value = current_value[semicolon_index+1:].strip()
                current_value = current_value.replace('"', '')
                map_dict[current_key] = current_value
            current_key, current_value = line.split(':', 1)
            current_key = current_key.strip()
            current_value = current_value.strip()
        else:
            current_value += ' ' + line.strip()

    if current_key:
        # Remove any double quotes and text before a semicolon in the value
        current_value = current_value.strip()
        semicolon_index = current_value.find(':')
        if semicolon_index != -1:
            current_value = current_value[semicolon_index+1:].strip()
        current_value = current_value.replace('"', '').replace(':', ' ')
        map_dict[current_key] = current_value

    return map_dict
def crop_thoughts(text):
    last_200 = text[-200:]  # Get the last 200 characters of the string

    # Find the index of the last period within the last 200 characters
    last_period_index = last_200.rfind('.')

    if last_period_index != -1:
        return last_200[:last_period_index+1]  # Return the portion of the string up to and including the last period
    else:
        return last_200  # If no period is found, return the entire last 200 characters

def response(personatags, chatlog):
    # Prepare the system script
    system = generation_script
    system = system.replace('<<PERSONA_TAGS>>', personatags)
    system = system.replace('<<RANDOM_SEED>>', str(uuid.uuid4()))
    system = system.replace('<<PERCENT>>', str(random.randint(1, 100)))

    # Get Response
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': chatlog})
    return gpt.execute(messages)

import functions_helper as file
import functions_kb as kb
import functions_chatlog as chat
def generate(userUUID, chatUUID, kbNames=[], profileNames={}, extra_tags={}):
    # Compile the tags
    persona_tags['Your Username'] = userUUID
    persona_tags['Language'] = 'English'
    persona_tags['Topic'] = 'No Topic Selected'

    # Get Chatlog
    chatlog = '\n\n'.join( chat.fetch(chatUUID, 'all_messages', 5)).strip()

    # Load Profiles
    #    Format: profileNames[ UUID ] = [ 'personality', 'emotional_state', 'attention', 'beliefs', 'preferences' ]
    persona_tags['People Nearby'] = '\n\nPeople that are here right now.\n'

    # Load bot thoughts
    profileNames[userUUID].append('latest_thoughts')

    for username, profile in profileNames.items():
        context = 'A Friend'
        if username == userUUID:
            context = 'THIS IS YOU'
        tagstring = f"<person uuid='{username}' relation_to_persona='{context}'>"

        for item in profile:
            content = file.open_file('Profiles/' + username + '.' + item + '.txt')
            privacy = 'public'
            if item.find('public') == -1:
                privacy = 'secret'
            if item.find('persona') != -1:
                privacy = 'pubic'
            tagstring += f"<attribute type='{item}' privacy='{privacy}'>{content}</attribute>"
        tagstring += "</person>\n"
        persona_tags['People Nearby'] += tagstring
    print('\n\nInformation about people:\n',persona_tags['People Nearby'])
    
    # Load Memories
    #    Format: kbNames = ['kb_one', 'kb_two']
    # persona_tags['Relavant Memories'] = '\n\n'
    # kbNames.append(userUUID)
    # kbNames.append(chatUUID)
    
    # for kb_index in kbNames:
    #     # Tell the bot where the memories are from
    #     context = 'Memories with unknown context'
    #     if kb_index == userUUID:
    #         context = 'Your Private Memories from your life'
    #     if kb_index == chatUUID:
    #         context = 'Memories of this conversation'
    #     if kb_index.find('public') == -1:
    #         context += '. THIS IS PRIVATE DO NOT SHARE DETAILS'
        
    #     # Get memories from kb search
    #     try:
    #         memories = kb.search(kb_index, chatlog, True)['Sorted_Filenames']

    #         # Extract files
    #         for filename in memories:
    #             filepath = f"KnowledgeBase/{kb_index}/{filename}"
    #             content = file.open_json(filepath, {"body":''})['body']
    #             persona_tags['Relavant Memories'] += f"<memory context='{context}'>{content}</memory>\n\n"

    #             # Cut off each KB
    #             if len(persona_tags['Relavant Memories']) > 500:
    #                 break
    #     except:
    #         print('Unable to load memories')
    
    

    # Generate Persona String
    personaTagString = ''
    for tagname, tagvalue in persona_tags.items():
        personaTagString += '<' + tagname + '>' + tagvalue + '</' + tagname + '>'
    for tagname, tagvalue in extra_tags.items():
        personaTagString += '<' + tagname + '>' + tagvalue + '</' + tagname + '>'

    # Get Responses
    draft_response = response(personaTagString, chatlog)
    print('\n\nBot is deciding what to say: \n', draft_response)
    response_object = create_map(draft_response)

    # Save new thoughts
    if 'ContextThoughts' in response_object:
        thoughts = file.open_file(f"Profiles/{userUUID}.latest_thoughts.txt")
        thoughts = crop_thoughts( thoughts + response_object['ContextThoughts'] )
        file.save_file(f"Profiles/{userUUID}.latest_thoughts.txt", thoughts)

    try:
        return_string = ''
        if 'Emotional_Reaction' in response_object:
            return_string += response_object['Emotional_Reaction'] + ' '
        
        
        if 'Final_Dialog' in response_object:
            print('\n\nBot decided on: \n', response_object['Final_Dialog'])
            return_string += response_object['Final_Dialog'] + ' '
        elif 'Possible_Dialog_Three' in response_object:
            print('\n\nBot decided on: \n', response_object['Possible_Dialog_Three'])
            return_string += response_object['Possible_Dialog_Three'] + ' '
        elif 'Possible_Dialog_Two' in response_object:
            print('\n\nBot decided on: \n', response_object['Possible_Dialog_Two'])
            return_string += response_object['Possible_Dialog_Two'] + ' '
        elif 'Possible_Dialog_One' in response_object:
            print('\n\nBot decided on: \n', response_object['Possible_Dialog_One'])
            return_string += response_object['Possible_Dialog_One'] + ' '
        else:
            return ''
        
        if 'Physical_Movement' in response_object:
            if response_object['Physical_Movement'] != 'None.':
                return_string += '( ' + userUUID + ' ' + response_object['Physical_Movement'] + ')'
        return return_string
    except:
        return ''


