import os
os.system('cls' if os.name == 'nt' else 'clear')

#
#   Helper Functions
#
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
def open_file(filepath,create_if_not_found=True):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
            return infile.read()
    except FileNotFoundError:
        if create_if_not_found:
            return ""
        else:
            raise

import json
def save_json(filepath, content):
    save_file(filepath, json.dumps(content))
def open_json(filepath, default_return=[]):
    # Load file
    data = open_file(filepath)
    if data == '':
        return default_return
    return json.loads(data)

def center_string(string, width):
    if len(string) >= width:
        return string  # No need for padding if string is already equal to or longer than the width
    string = ' ' + string + ' '
    padding = width - len(string)
    left_padding = padding // 2
    right_padding = padding - left_padding

    centered_string = ' ' * left_padding + string + ' ' * right_padding
    return ' |' + centered_string + '|'
def inputBool(prompt):
    while True:
        user_input = input(prompt)
        if user_input.upper() == 'Y':
            return 'Y'
        elif user_input.upper() == 'N':
            return 'N'
        else:
            print("Invalid input. Please enter 'Y' or 'N'")

#
#   Profile management
#
userProfileDirectory = 'gpt_profiles'
def userInit(profile_name):
    data = open_file(userProfileDirectory + '/' + profile_name + '.txt')
    return data

#
#   Chatlog management
#
chatLogDirectory = 'chatdb'
def chatSync(chatlog_name, catagory):
    # Store under catagory
    profile = chatlog_name + '-' + catagory
    filepath = chatLogDirectory + '/' + profile + '.json'

    # Return the log
    return open_json(filepath, [])
def chatFetch(chatlog_name, catagory, entries=3):
    # Load
    chatlog = chatSync(chatlog_name, catagory)
    # Splice
    if (entries==-1):
        return chatlog
    if entries >= len(chatlog):
        return chatlog
    else:
        return chatlog[-entries:]

import subprocess
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

def lnfeed():
    print('\n')

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('<========================================================>')
    print(center_string(' ', 54))
    print(center_string('~~Welcome to the group chat~~', 54))
    print(center_string('To get started we need some info', 54))
    print(center_string(' ', 54))
    print('<========================================================>')
    lnfeed()

    apikey = input('Whats your OpenAI key: ')
    apikey = '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'
    lnfeed()

    # Get user
    current_user = input('Username you will identify with: ')
    if current_user == '':
        current_user = 'DefaultUser'
    profile = userInit(current_user)
    if profile == '':
        print(' * This profile does not exist, Creating new profile for ' + current_user)
    else:
        print(' * Welcome back, ' + current_user)
    lnfeed()

    # Get bot
    current_bot = input('Username the bot identify with: ')
    if current_bot == '':
        current_bot = 'DefaultBot'

    profile = userInit(current_bot)
    if profile != '':
        print(' * Bot Found: ' + current_bot)
    else:
        print(' * Bot not found: ' + current_bot)
        # @TODO Select a persona and copy that to the bots name
    lnfeed()

    answer = input('Load Settings (blank=default_settings, anything_else=advanced):')
    if (answer == ''):
        answer = 'default_settings'
    
    settings = open_json('converse_settings/' + answer + '.json', {})
    if settings == {}:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('<========================================================>')
        print(center_string('~~Settings Wizard~~', 54))
        print(center_string(' ', 54))
        print(center_string('Questions about your interactions', 54))
        print(center_string(' ', 54))
        print('<========================================================>')
        lnfeed()
        
        print('Do you want to develop a profile?')
        print('    Example: catmonster - Your words will will modify the profile')
        settings['user_saveprofile'] = input('Profile Names (comma seperated list with no spaces, blank=skip)?')
        settings['user_freezeprofile'] = inputBool('Make your personal profile READONLY (Y/N)?')
        lnfeed()

        print('Do you want develop a persona?')
        print('    Example: catmonster - Your behavior will will modify the persona')
        settings['user_savepersona'] = input('Persona Names (comma seperated list with no spaces, blank=skip)?')
        settings['user_freezepersona'] = inputBool('Make your personal persona READONLY (Y/N)?')
        lnfeed()

        print('Do you want to develop a memory database?')
        print('    Example: catmonster - The catmonster will remember this session')
        settings['user_savekbs'] = input('Repo Names (comma seperated list with no spaces, blank=skip)')
        settings['user_freezekb'] = inputBool('Make your personal memories READONLY (Y/N)?')
        lnfeed()

        os.system('cls' if os.name == 'nt' else 'clear')
        print('<========================================================>')
        print(center_string('~~Settings Wizard~~', 54))
        print(center_string(' ', 54))
        print(center_string('Customize Your Bot', 54))
        print(center_string(' ', 54))
        print('<========================================================>')
        lnfeed()

        print('Load additional profiles for the bot?')
        print('    The bot will think it is a mix of iteself and the loaded profiles')
        print('    Example: otherbotname')
        print('    WARNING: Bot may mix up facts about itself permenently if not set to READONLY on next step )')
        settings['bot_saveprofile'] = input('Profile Names (comma seperated list with no spaces, blank=skip)?')
        settings['bot_freezeprofile'] = inputBool('Make bots personal profile READONLY (Y/N)?')
        lnfeed()

        print('Override bots persona?')
        print('    Example: catmonster')
        print('    WARNING: Bot may pick up random habits permenently from its behavior if not set to READONLY')
        settings['bot_persona'] = input('Override with (blank=no-override)?')
        settings['bot_freezepersona'] = inputBool('Make bots personal persona READONLY (Y/N)?')
        lnfeed()

        print('Who does the bot know?')
        print('    WARNING: Pure usernames will allow access to private information')
        print('    ^ User can make a pubic profile which is the one that should be here')
        settings['bot_knownusers'] = input('List of people profiles (comma seperated list with no spaces, blank=skip)')
        lnfeed()

        print('Forget this conversation when not in the conversation?')
        print('    * Bot will not carry memories outside this conversation')
        settings['bot_freezekb'] = inputBool('Make bots personal memorys READONLY (Y/N)?')
        lnfeed()

        print('Which Memory Repos does this bot have READONLY access too?')
        print('    Tip: Develop a memory repo with "kb_add_memory.py" or by "building a memory repo"')
        settings['bot_knownkbs'] = input('List of repos (comma seperated list with no spaces, blank=skip)')
        lnfeed()

        settings['action'] = 'default_chat'
        settings['language'] = 'english'
        settings['topic'] = 'None'

        answer = input('Save these settings (Name, blank=skip): ')
        if answer != '':
            save_json('converse_settings/' + answer + '.json', settings)





    # Choose chat
    current_chat = input('Enter the name of the chat: ')
    if current_chat == '':
        current_chat = 'main'
    chatlog = chatFetch(current_chat,'all_messages',-1)
    chatlength = str(len(chatlog))

    while True:
        # Print system message
        os.system('cls' if os.name == 'nt' else 'clear')
        print('<========================================================>')
        print(center_string('Welcome to the chat!', 54))
        print(center_string(' ', 54))
        print(center_string('Currently Chatting', 54))
        print(center_string('User: ' + current_user + ' Bot:' + current_bot, 54))
        print(center_string(' ', 54))
        print(center_string('Conversation is saved to: ' + current_chat, 54))
        print(center_string('Conversation Length: ' + chatlength, 54))
        print(center_string(' ', 54))
        print(center_string('API Key: ' + apikey, 54))
        print(center_string(' ', 54))
        print('<========================================================>')
        chatlog = chatFetch(current_chat, 'all_messages', 10)
        for message in chatlog:
            print(message)

        # get user input
        current_dialog = input('USER: ')

        #
        #   Add Chat
        #
        arguments = list()
        arguments.extend(["-apikey", apikey])

        arguments.extend(["-userUUID", current_user])
        arguments.extend(["-chatUUID", current_chat])
        arguments.extend(["-dialog", current_dialog])
        

        # Optional arguments
        arguments.extend(["-savekbs", settings['user_savekbs']])
        arguments.extend(["-savepersona", settings['user_savepersona']])
        arguments.extend(["-saveprofile", settings['user_saveprofile']])
        
        arguments.extend(["-freezekb", settings['user_freezekb']])
        arguments.extend(["-freezepersona", settings['user_freezepersona']])
        arguments.extend(["-freezeprofile", settings['user_freezeprofile']])

        script_path = "chat_add_response.py"

        print('Adding User Repsonse To Chat')
        success = run_script_with_output(script_path, arguments)
        print(success)

        #
        #   Facilitate Response
        #
        arguments = list()
        arguments.extend(["-apikey", apikey])

        arguments.extend(["-userUUID", current_bot])
        arguments.extend(["-chatUUID", current_chat])
        

        # Optional arguments
        # arguments.extend(["-savekbs", settings['bot_savekbs']])
        # arguments.extend(["-savepersona", settings['bot_savepersona']])
        arguments.extend(["-saveprofile", settings['bot_saveprofile']])

        arguments.extend(["-freezekb", settings['bot_freezekb']])
        arguments.extend(["-freezepersona", settings['bot_freezepersona']])
        arguments.extend(["-freezeprofile", settings['bot_freezeprofile']])

        arguments.extend(["-knownusers", settings['bot_knownusers']])
        arguments.extend(["-knownkbs", settings['bot_knownkbs']])
        arguments.extend(["-persona", settings['bot_persona']])

        # arguments.extend(["-action", settings['action']])
        # arguments.extend(["-lang", settings['language']])
        # arguments.extend(["-topic", settings['topic']])

        script_path = "chatbot_gen.py"

        print('Adding Bots Repsonse To Chat')
        success = run_script_with_output(script_path, arguments)
        print(success)

        input('Press enter to continue.')
