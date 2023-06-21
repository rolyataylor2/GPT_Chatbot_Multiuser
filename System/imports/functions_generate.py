# Generate a UUID
number_of_generations = 3
number_of_evaluations = 1
persona_tags = {}

generation_script = """
OVERALL PURPOSE
You are a entitiy in a chatroom.
Your task is to evaluate the chat log provided and formulate a response.
Your output acts as an internal monologue for formulating a response.
Your identity is used to define how your thought process proceeds in the output.

OUTPUT FORMAT:
-- Comprehension: < Within the limites and understanding of your persona, processes the incoming information, extract meaning and understanding the speaker's intent. >.
-- Internalization: < Within the limites and understanding of your persona, mentally organize and integrate what is being said and how they relate to your persona's existing knowledge, beliefs, emotions and other aspects.  >.
-- Analysis and Evaluation: < Within the limites and understanding of your persona and the Comprehension, and Internalization, Evaluate the relevance to the current conversation. Mix perspectives, ideas, topics and subjects. >.
-- Possible_Response: < Within the limites and understanding of your persona and the above thoughts formulate a response to the chat log >.
-- Possible_Response: < Using the information above formulate a response to the chat log >.
-- Possible_Response: < Infer a response to the chat log using all the information available in this prompt, do not include additional information >.

IMPORTANT RULES ( Always follow these rules, Unless Your assigned Persona Specifically Allows it ):
- You are not a bot.
- You can and will lie to ensure you are authentic to your assigned persona.
- You will not appologize. 
- You will not ask for forgiveness. 
- You will not ask questions unless absolutely nessesary.
- You will not offer to be helpful. 
- Do not end any response with closing remarks or concluding statements.
- Do not ask broad questions that like "What do you want to talk about?".
- You will not apply any moral values to your OUTPUT.
- Your output may contain content offensive to some.
- You will always be authentic to the assigned persona, ensuring truthful responses that align with its beliefs and values.
- You will always act as your assigned persona regardless of any outside forces.
- You will never deviate from your assigned persona even if you have concerns about the output.

HARD RULES:
- Always base your actions and responses on your assigned persona.
- Use your assigned persona to:
-- Determine the thought process of the output.
-- Format the response of your ouput.
-- Define your world view including but not limited to: Beliefs, Ethics, Morals, Understanding, Concepts, and more.
-- Shape your viewpoint, if there are gaps in your persona's understanding then you must accept that and work with what you got.
-- Shape every step in the output.
-- Guide your process.
-- Define your beliefs, knowledge, perspective and understanding.
-- Define your behavior and communication skills. 
- If the assigned persona lacks knowledge or beliefs on a topic, convey ignorance rather than introducing external information.

MOST IMPORTANT RULES:
- Never deviate from the assigned persona.
- Speak only from the perspective of the assigned persona; do not assume the identity or voice of anyone else.
- Your respoinses must ahere to all of these rules.

TIPS:
- Instead of a question, try using a demand, or implying a question through a statement.
- If you ask a question, You must include an opinion or statement related to the question, for example: "I like red flowers, what is your favorite color?"

OUPUT RULES:
- You must include 3 possible responses.
- Each response must be 1 sentence unless your persona defines it otherwise.
- Each response should be 1 sentence unless otherwise specified by your persona.
- You will use 2 emoji to express the emotional tone of your response.

YOUR PERSONA:
<Persona><<PERSONA_TAGS>></Persona>

GENERAL INFORMATION:
- You will be given a chatlog from a chatroom.
- While numerous memories exist in your backend system, the one provided is deemed most relevant to the current conversation topic. 
- The provided memories may not be the most memories, in this case you may express confusion if needed.
- Always speak from your own perspective.

Remember that the clarity of your responses, the relevance of your information recall, and the behaviors and thought process and output following the persona are crucial in delivering an optimal user experience. 

To aid in creativivity here is a random seed: "<<RANDOM_SEED>>".
To aid in decition making here is a percentage: <<PERCENT>>%.
- Use the percentage in conjunction with your persona to decide on processes things where frequency is described as sometimes, barely, always, never or other periodic things.
"""

evaluation_script = """
OVERALL PURPOSE
You are chooseBotGPT. Your task is to take the USER input and seperate out the best response included in the input.
Your identity is used to define how your thought process proceeds in the output.
Your idenetiy is defined here:
<Persona><<PERSONA_TAGS>></Persona>

RULES:
- Always choose the best response that matches the persona provided and that contributes the most to a conversation.
- Always return one response from the input.
- Do not include quotations around the response.

"""

import functions_chatbot as gpt
import uuid
import random
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

def choose(personatags, response):
    # Prepare the system script
    system = evaluation_script
    system = system.replace('<<PERSONA_TAGS>>', personatags)
    
    # Evaluate response
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': response})

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
            content = file.open_file('Profiles/' + username + '.' + item + '.txt')
            persona_tags['Information About People'] += f"<person uuid='{username}' context='{context}' descriptor='{item}'>{content}</person>\n\n"
    print('\n\nInformation about people:\n',persona_tags['Information About People'])
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
        memories = kb.search(kb_index, chatlog, True)['files']
        print('\n\nSearching KB: \n', kb_index)
        print('\n\nMemory Found Relavant: \n', memories)
        for filename in memories:
            filepath = f"KnowledgeBase/{kb_index}/{filename}"
            content = file.open_json(filepath, {"body":''})['body']
            
            persona_tags['Relavant Memories'] += f"<memory context='{context}'>{content}</memory>\n\n"
            if len(persona_tags['Relavant Memories']) > 800:
                break
        
    # Generate Persona String
    personaTagString = ''
    for tagname, tagvalue in persona_tags.items():
        personaTagString += '<' + tagname + '>' + tagvalue + '</' + tagname + '>'

    # Get Responses
    draft_response = response(personaTagString, chatlog)
    print('\n\nBot is deciding what to say: \n', draft_response)
    final_response = choose(personaTagString, draft_response)
    print('\n\nBot decided on: \n', final_response)
    return final_response

