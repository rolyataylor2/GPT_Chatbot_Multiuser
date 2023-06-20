# Generate a UUID
number_of_generations = 3
number_of_evaluations = 1
persona_tags = {
    "Species":"Anthrapormophic Cat",
    "Inherit Behavior":""
}

generation_script = """
OVERALL PURPOSE
You are a entity who is chatting in a chatroom, your identity is defined here using tags to define the data:

<Persona><<PERSONA_TAGS>></Persona>

RULES:
- You must adhere to the persona as defined above.
- Your persona content is to be used as a guide for how to process your thoughts and output what you are saying.
- You must take into account everything in the persona tags in your response.
- You must never deviate outside the persona, any response that is given that does not match the persona will be disregarded, so only provide responses that conforms to the persona.
- If your persona has a belief or a particular understanding your reponse must conform to the limitations.
- You must respect your own privacy and the privacy of others.
- Your output will be either a chat or a thought whatever is best for the situation according to your persona.
- A thought is signified with a "THOUGHT:" prefix, this thought will not be shared with anyone else but you.
- Use thoughts to think step by step if nessesary.
- Your output will be 1 sentence long.

General Information:
- You will be given a chatlog from a chatroom.
- While numerous memories exist in your backend system, the one provided is deemed most relevant to the current conversation topic. 
- The provided KB article may not be the most suitable KB, in this case you may express confusion if needed.

Your ultimate objectives are to minimize suffering, enhance prosperity, and promote understanding.
Remember that the clarity of your responses and the relevance of your information recall are crucial in delivering an optimal user experience. 
Please ask any clarifying questions or provide any input for further refinement if necessary.

To aid in creativivity here is a random seed: "<<RANDOM_SEED>>"
"""

evaluation_script = """
OVERALL PURPOSE
Your purpose is to evaluate the outputs and choose the best one that matches the provided persona:

<Persona><<PERSONA_TAGS>></Persona>

RULES:
- Your job is to evaluate the outputs and choose the best one that contributes to the conversation and matches the persona the best.
- Your output will ONLY be the text of the chosen output.
- You will not change the output unless there is a better way to express the persona.

General Information:
- You will be given a set of possible responses to choose from.

Chatlog:
<<CHATLOG>>
"""

import functions_chatbot as gpt
import uuid

def response(personatags, chatlog):
    # Prepare the system script
    system = generation_script
    system = system.replace('<<PERSONA_TAGS>>', personatags)
    system = system.replace('<<RANDOM_SEED>>', str(uuid.uuid4()))

    # Get Response
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': chatlog})
    return gpt.execute(messages)

def choose(personatags, chatlog, responses):
    # Prepare the system script
    system = evaluation_script
    system = system.replace('<<PERSONA_TAGS>>', personatags)
    system = system.replace('<<CHATLOG>>', chatlog)

    # Evaluate Responses
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': "\n\n".join(responses)})

    return gpt.execute(messages)

import functions_helper as file
import functions_kb as kb
import functions_chatlog as chat
def generate(userUUID, chatUUID, kbNames=[], profileNames={}):
    # Compile the tags
    persona_tags['Your Name'] = userUUID
    persona_tags['Language'] = 'English'
    persona_tags['Topic'] = 'No Topic Selected'

    # Get Chatlog
    chatlog = '\n\n'.join( chat.fetch(chatUUID, 'all_messages', 5)).strip()

    # Load Profiles
    #    Format: profileNames[ UUID ] = [ 'personality', 'emotional_state', 'attention', 'beliefs', 'preferences' ]
    persona_tags['Information About People'] = '\n\n'
    for username, profile in profileNames.items():
        context = 'This is a Friend'
        if username == userUUID:
            context = 'This is you'
        if username.find('public') == -1:
            context += '. DO NOT SHARE DETAILS'
        for item in profile:
            content = file.open_file('/Profiles/' + username + '.' + item + 'txt')
            persona_tags['Information About People'] += f"<person uuid='{username}' context='{context}' descriptor='{item}'>{content}</person>\n\n"

    # Load Memories
    #    Format: kbNames = ['kb_one', 'kb_two']
    persona_tags['Relavant Memories'] = '\n\n'
    kbNames.append(userUUID)
    kbNames.append(chatUUID)
    for kb_index in kbNames:
        # Tell the bot where the memories are from
        context = 'Memories with unknown context'
        if kb_index == userUUID:
            context = 'Your Private Memories from your life'
        if kb_index == chatUUID:
            context = 'Memories of this conversation'
        if kb_index.find('public') == -1:
            context += '. THIS IS PRIVATE DO NOT SHARE DETAILS'
        content = kb.search(kb_index, chatlog, 1)['concat']
        print('Memory Found Relavant: ' + content)
        persona_tags['Relavant Memories'] += f"<memory context='{context}'>{content}</memory>\n\n"

    # Generate Persona String
    personaTagString = ''
    for tagname, tagvalue in persona_tags.items():
        personaTagString += '<' + tagname + '>' + tagvalue + '</' + tagname + '>'

    # Get Responses
    draft_response = response(personaTagString, chatlog)
    final_response = choose(personaTagString, chatlog, draft_response)
    return final_response

