#
# Help screen and get arguments
#

import argparse
from argparse import RawTextHelpFormatter
import os
RESET = '\033[0m'
GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
description = RED + 'Multi-user Chatbot using GPT\n' + RESET
description += '   ' + GREEN + 'Action:' + RESET + ' Generates Bot Response to chatroom\n'
description += '           Saves that response to chatroom\n'
description += '           Adds Memories, Updates Profiles, and Updates Personas\n'
description += '   ' + GREEN + 'Returns:' + RESET + ' void 0\n\n'
description += '   ' + GREEN + 'Purpose:' + RESET + '\n'
description += '           Use this script to generate and post dialog to the chat $chatUUID under the identity as defined by $userUUID\n\n'
parser = argparse.ArgumentParser(description=description, usage='"%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)

# Required arguments
parser.add_argument("-userUUID", metavar=' ', help='User-UUID', required=True)
parser.add_argument("-chatUUID", metavar=' ', help='Chatroom-UUID', required=True, default='general')
parser.add_argument("-apikey", metavar=' ', required=True, help="Your OpenAI API key.\n" + RED + "CAUTION:" + RESET + " $$$\n ")

# Optional arguments
parser.add_argument("-savekbs", metavar=' ', required=False, default='', help="Merge Into Additional KBs:\n" + GREEN + "Type:" + RESET + " Comma-Delimited-List\n" + GREEN + "Always updates:" + RESET + " $chatUUID,$userUUID\n ")
parser.add_argument("-savepersona", metavar=' ', required=False, default='', help="Merge Additional Personas\n" + GREEN + "Type:" + RESET + " Comma-Delimited-List\n" + GREEN + "Always updates:" + RESET + " $userUUID\n ")
parser.add_argument("-saveprofile", metavar=' ', required=False, default='', help="Merge Additional Profiles\n" + GREEN + "Type:" + RESET + " Comma-Delimited-List\n" + GREEN + "Always updates:" + RESET + " $userUUID\n ")

parser.add_argument("-knownusers", metavar=' ', required=False, default='', help="Profiles of bots friends\n" + GREEN + "Always has access to:" + RESET + " $userUUID\nIf the name contains 'public' the bot will not try to hide details\n" + RED + "CAUTION:" + RESET + " Pure UUIDs are private, Bots cant keep secrets\n ")
parser.add_argument("-knownkbs", metavar=' ', required=False, default='', help="Memory Databases for the bot\n" + GREEN + "Always has access to:" + RESET + " $userUUID\n" + RED + "CAUTION:" + RESET + "These are not kept secret\n ")

parser.add_argument("-freezekb", metavar=' ', required=False, default='N', help="Dont write personal KBs")
parser.add_argument("-freezepersona", metavar=' ', required=False, default='N', help="Dont write personal persona")
parser.add_argument("-freezeprofile", metavar=' ', required=False, default='N', help="Dont write personal profile")

parser.add_argument("-action", metavar=' ', required=False, default='default_chat', help="Action to be taken from the gpt_actions directory")
parser.add_argument("-language", metavar=' ', required=False, default='english', help="Language that the bot should use. Default is 'English'")
parser.add_argument("-persona", metavar=' ', required=False, default='', help="Override bots persona using one from 'gpt_personas' directory")
parser.add_argument("-topic", metavar=' ', required=False, default='No Topic Selected', help="Set a topic to talk about")
args = parser.parse_args()

import subprocess
import os

def run_script_with_output(script_path, arguments=[]):
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the script
    absolute_path = os.path.join(current_dir, script_path)

    # Construct the command to execute the script
    command = ["python3", absolute_path] + arguments

    try:
        # Run the script and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the script executed successfully
        if result.returncode == 0:
            # Return the output of the script
            return result.stdout
        else:
            # Print the error output if the script had a non-zero return code
            print(result.stderr)
    
    except subprocess.CalledProcessError as e:
        # Handle any exception that occurred during the subprocess execution
        print(f"Error running script: {e}")
    
    return None

if __name__ == '__main__':
    #
    #   Generate the text
    #
    arguments = list()
    arguments.extend(["-userUUID", args.userUUID])
    arguments.extend(["-chatUUID", args.chatUUID])
    arguments.extend(["-apikey", args.apikey])

    arguments.extend(["-knownusers", args.knownusers])
    arguments.extend(["-knownkbs", args.knownkbs])

    arguments.extend(["-action", args.action])
    arguments.extend(["-language", args.language])
    arguments.extend(["-persona", args.persona])
    arguments.extend(["-topic", args.topic])

    script_path = "chatbot_gen_response.py"
    generated_text = run_script_with_output(script_path, arguments)


    #
    #   Save to chatroom
    #
    # Required arguments
    arguments = list()
    arguments.extend(["-userUUID", args.userUUID])
    arguments.extend(["-chatUUID", args.chatUUID])
    arguments.extend(["-apikey", args.apikey])
    arguments.extend(["-dialog", generated_text])

    # Optional arguments
    arguments.extend(["-savekbs", args.savekbs])
    arguments.extend(["-savepersona", args.savepersona])
    arguments.extend(["-saveprofile", args.saveprofile])

    arguments.extend(["-freezekb", args.freezekb])
    arguments.extend(["-freezepersona", args.freezepersona])
    arguments.extend(["-freezeprofile", args.freezeprofile])

    script_path = "chat_add_response.py"
    run_script_with_output(script_path, arguments)
