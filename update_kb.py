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
description += '    ' + term.colorGreen('Action:') + ' Updates the knowledge based from chats from the chatUUID\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)

# Arguments
parser.add_argument("-userUUID", metavar=' ', help='User-UUID', required=True)
parser.add_argument("-chatUUID", metavar=' ', help='Chatroom-UUID', required=True, default='general')
parser.add_argument("-selection", metavar=' ', required=False, default=-5, help="Select the chats (5=first five, -5=last five, 0=all )\n")
parser.add_argument("-savekbs", metavar=' ', required=False, default='', help="Merge Into Additional KBs:\n" + term.colorGreen("Type:") + " Comma-Delimited-List\n" + term.colorGreen("Always updates:") + " $chatUUID,$userUUID\n ")
parser.add_argument("-freezekb", metavar=' ', required=False, default='N', help="Dont write default KBs")
args = parser.parse_args()

#
#   Script Begins
#
import functions_chatlog as chatlog
import functions_kb as kb

if __name__ == '__main__':
    # UUID of user and bot, bots are treated as users
    current_user = args.userUUID
    current_chat = args.chatUUID
    selection = int(args.selection)

    # Fetch conversation
    latest_conversation = '\n\n'.join( chatlog.fetch( current_chat, 'all_messages', selection )).strip()

    # Save memories ot kbs
    save_kbs = args.savekbs.split(',')
    if args.savekbs == '':
        save_kbs = []
    if args.freezekb == 'N':
        save_kbs.append(current_user)
        save_kbs.append(current_chat)
    
    # Update KBs
    kb.update(save_kbs, latest_conversation)

    