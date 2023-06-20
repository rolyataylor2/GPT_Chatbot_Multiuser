#
# Imports
#
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/System/imports')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/System/gpt-observers')

import argparse
from argparse import RawTextHelpFormatter
import functions_termcolors as term

# App Description
description = term.colorRed('Multi-user Chatbot using GPT\n')
description += '    ' + term.colorGreen('Action:') + ' Generates a response the the context of $chatUUID with the identity of $userUUID\n'
description += '        Bot will attempt to follow direction of $action from the gpt_actions directory.\n'
description += '        This script does not modify any long term data.\n\n'
description += '        ' + term.colorYellow('Returns:') + ' <string> One Chatbot Response to a chatroom conversation.\n\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)

# Arguments
parser.add_argument("-userUUID", metavar=' ', help='User-UUID', required=True)
parser.add_argument("-chatUUID", metavar=' ', help='Chatroom-UUID', required=True, default='general')

parser.add_argument("-knownusers", metavar=' ', required=False, default='', help="Profiles of bots friends\n" + term.colorGreen("Always has access to:") + " $userUUID\nIf the name contains 'public' the bot will not try to hide details\n" + term.colorRed('CAUTION:') + " Pure UUIDs are private, Bots cant keep secrets\n ")
parser.add_argument("-knownkbs", metavar=' ', required=False, default='', help="Memory Databases for the bot\n" + term.colorGreen("Always has access to:") + " $userUUID\n" + term.colorRed('CAUTION:') + "These are not kept secret\n ")

parser.add_argument("-action", metavar=' ', required=False, default='default_chat', help="Action to be taken from the gpt_actions directory")
parser.add_argument("-language", metavar=' ', required=False, default='english', help="Language that the bot should use. Default is 'English'")
parser.add_argument("-persona", metavar=' ', required=False, default='', help="Override bots persona using one from 'gpt_personas' directory")
parser.add_argument("-topic", metavar=' ', required=False, default='No Topic Selected', help="Set a topic to talk about")
args = parser.parse_args()

#
#   Script Begins
#


import functions_chatbot as chatbot
import functions_kb as kb
import functions_chatlog as chatlog
import functions_profile as profile
chatActionDirectory = 'System/gpt-actions'


if __name__ == '__main__':
    # Action to take
    chatbot_action_script = chatbot.getScript(chatActionDirectory + args.action)

    # UUID of user and bot, bots are treated as users
    current_user = args.userUUID
    chatbot_action_script = chatbot_action_script.replace('<<UUID>>', current_user) # So the bot knows who it is in the conversation

    # Load Persona
    chatbot_persona = current_user + '.persona'
    if args.persona != '':
        chatbot_persona = args.persona
    chatbot_persona = profile.get(chatbot_persona)
    chatbot_action_script = chatbot_action_script.replace('<<PERSONA>>', chatbot_persona) # What persona to take on

    # Load the chat
    current_chat = args.chatUUID

    # 
    #   Load Profiles
    #
    known_profiles = args.knownusers.split(',')
    if args.knownusers == '':
        known_profiles = []
    known_profiles.append(current_user)

    person_profiles = list()
    for profile_name in known_profiles:
        label = 'This is a Friend'
        if profile_name == current_user:
            label = 'This is you'
        if profile_name.find('public') == -1:
            label += '. DO NOT SHARE DETAILS'
        
        # Load the profile
        profile_text = profile.get(profile_name)
        if profile_text != '':
            person_profiles.append('<person context="' + label + '">' + profile_text + '</person>')

    chatbot_action_script = chatbot_action_script.replace('<<PROFILES>>', ''.join(person_profiles)) # Friends and people you know

    # 
    #   Load KBs
    #
    known_kb = args.knownkbs.split(',')
    if args.knownkbs == '':
        known_kb = []
    known_kb.append(current_user)
    known_kb.append(current_chat)

    search_term = chatlog.fetch(current_chat, 'all_messages', 5) # Get the log of current conversation
    search_term = '\n\n'.join(search_term).strip() # Convert into a string
    kb_articles = list()
    for kb_name in known_kb:
        # Tell the bot where the memories are from
        label = 'Memories with unknown context'
        if kb_name == current_user:
            label = 'Your Private Memories from your life'
        if kb_name == current_chat:
            label = 'Memories of this conversation'
        if kb_name.find('public') == -1:
            label += '. THIS IS PRIVATE DO NOT SHARE DETAILS'
        # Search the memories
        kb_text = kb.search(kb_name, search_term, 1)['concat']
        if kb_text != "No new KB article could be created based on the given chat logs.":
            kb_articles.append( '<memory from="' + label + '">' + ''.join(kb_text) + '</memory>' ) # Fetch One Relavant conversation from the database

    chatbot_action_script = chatbot_action_script.replace('<<KB>>', ''.join(kb_articles)) # Plop some memories in there

    #
    #   Load other vars
    #
    conversation_topic = args.topic
    conversation_language = args.language
    chatbot_action_script = chatbot_action_script.replace('<<TOPIC>>', ''.join(conversation_topic)) # Topic?
    chatbot_action_script = chatbot_action_script.replace('<<LANG>>', ''.join(conversation_language)) # Language
    chatbot_action_script = chatbot_action_script.replace('\n',' ').replace('  ',' ')
    
    #
    #   Execute conversation and recieve output
    #
    current_conversation = list()
    current_conversation.append( {'role': 'system', 'content': chatbot_action_script} )
    current_conversation.extend( chatlog.fetch(current_chat, 'conversation', -1) )

    response = chatbot.execute(current_conversation)
    print(response)
