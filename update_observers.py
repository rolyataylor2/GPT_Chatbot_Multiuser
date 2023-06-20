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
description += '    ' + term.colorGreen('Action:') + ' Updates the persona of a userUUID using the text from chatUUID\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)

# Arguments
parser.add_argument("-userUUID", metavar=' ', help='User-UUID', required=True)
parser.add_argument("-chatUUID", metavar=' ', help='Chatroom-UUID', required=True, default='general')
parser.add_argument("-observers", metavar=' ', required=False, default='', help="A list of observers to run. ")
args = parser.parse_args()



#
#   Script Begins
#
import functions_chatlog as chatlog

if __name__ == '__main__':
    # UUID of user and bot, bots are treated as users
    current_user = args.userUUID
    current_chat = args.chatUUID

    # Upate Personas
    current_observers = args.observers.split(',')
    if args.observer == '':
        current_observers = []
        
    # Run the observer
    for observer_name in current_observers:
        try:
            import observer_name as observer
            observer.Analyse(current_user, current_chat)
            print('Ran: ', observer_name)
        except:
            print('Ran: ', observer_name, ' FAILED')

