#
# Imports
#
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/System/imports')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/System/gpt-observers')
os.system('cls' if os.name == 'nt' else 'clear')

import functions_helper as file
import functions_observer as observer
import functions_chatlog as chat
import functions_generate as bot

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

    # Get user
    current_user = input('Username you will identify with: ')
    if current_user == '':
        current_user = 'DefaultUser'
        print('    You are being assigned: ', current_user)
    lnfeed()

    # Get bot
    current_bot = input('Username the bot identify with: ')
    if current_bot == '':
        current_bot = 'DefaultBot'
        print('    The bot is being assigned: ', current_bot)
    lnfeed()

    answer = input('Load Settings (blank=default_settings, anything_else=advanced):')
    if (answer == ''):
        answer = 'default_settings'
    settings_directory = 'System/settings/'
    settings = file.open_json(settings_directory + answer + '.json', {})
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
            file.save_json(settings_directory + answer + '.json', settings)





    # Choose chat
    current_chat = input('Enter the name of the chat: ')
    if current_chat == '':
        current_chat = 'main'
    chatlog = chat.fetch(current_chat,'all_messages',-1)
    chatlength = str(len(chatlog))
    def format_user_input(text):
        # Split the text into username and user message
        username, message = text.split(': ')

        # Calculate the sum of ASCII values of the username characters
        ascii_sum = sum(ord(char) for char in username) * 3

        # Calculate the text color based on the ASCII sum (0-255)
        text_color = ascii_sum % 256

        # Calculate the background color by subtracting a fixed value (e.g., 40) from the text color
        background_color = (text_color - 40) % 256

        # Calculate the font color as the opposite of the background color
        font_color = (background_color + 128) % 256

        # Format the username with the calculated font and background colors, and left-justify
        formatted_username = f'\033[38;5;{font_color};48;5;{background_color}m{username.ljust(15)}\033[0m'

        # Align the message to 15 spaces from the beginning
        lines = []
        current_line = ''
        for word in message.split(' '):
            if len(current_line) + len(word) < 80:
                current_line += word + ' '
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        lines.append(current_line.strip())
        formatted_message = '\n'.join([lines[0]] + [' ' * 13 + line for line in lines[1:]])

        # Combine the formatted username and message
        formatted_text = f'{formatted_username}: {formatted_message}'

        return formatted_text


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
        print('<========================================================>')
        print(current_user, 'Mood: ', observer.get_observation('Track_Mood', current_user))
        print(current_bot, 'Mood: ', observer.get_observation('Track_Mood', current_bot))
        lnfeed()

        chatlog = chat.fetch(current_chat, 'all_messages', 10)
        for message in chatlog:
            print(format_user_input(message))

        # get user input
        current_dialog = input('Reply: ')

        #
        #   Add Human Chat
        #
        print('Adding User Repsonse To Chat...')
        chat.add(current_chat, 'user_' + current_user, current_dialog) # Add user message to personal log
        chat.add(current_chat, 'all_messages', current_user + ': ' + current_dialog) # Add user message to merged conversation log
        chat.add(current_chat, 'conversation', {'role': 'user', 'content': current_user + ': ' + current_dialog})

        #
        #   Generate a bot response
        #
        known_kb = settings['bot_knownkbs'].split(',')
        if settings['bot_knownkbs'] == '':
            known_kb = []

        known_profiles = {}
        known_profiles[ current_bot ] = [ 'persona', 'Emotional_State', 'Preferences' ]
        known_profiles[ current_user ] = [ 'Emotional_State', 'Preferences' ]
        print('\n\nGenerating Bots Repsonse To Chat...')
        generated_text = bot.generate(current_bot, current_chat, known_kb, known_profiles)

        #
        #   Add Bot Chat
        #
        print('\n\nAdding Bots Repsonse To Chat...')
        chat.add(current_chat, 'user_' + current_bot, generated_text) # Add user message to personal log
        chat.add(current_chat, 'all_messages', current_bot + ': ' + generated_text) # Add user message to merged conversation log
        chat.add(current_chat, 'conversation', {'role': 'user', 'content': current_bot + ': ' + generated_text})

        #
        #   Run observers
        #
        print('\n\nAnalysing mood...')
        observer.observe('Track_Mood', current_user, current_chat)
        observer.observe('Track_Mood', current_bot, current_chat)
        observer.observe('Get_Preferences', current_user, current_chat)
        observer.observe('Get_Preferences', current_bot, current_chat)
        #
        #   Generate KB
        #
        arguments = list()
        arguments.extend(["-userUUID", current_user])
        arguments.extend(["-chatUUID", current_chat])
        arguments.extend(["-selection", '5'])

        savekbs = settings['user_savekbs'] + ','
        if savekbs == ',':
            savekbs = ''
        savekbs += ('-'.join([current_user, current_bot]))
        savekbs += ',' + current_bot
        arguments.extend(["-savekbs", savekbs]) # Also include current_user + current_bot << sort by name though or else youll have to make 2 copies
        arguments.extend(["-freezekb", 'N'])

        print('\n\nCreating a memory of the chat...')
        success = run_script_with_output("update_kb.py", arguments)
        print(success)

        #
        #    Update Observations
        #
        

        input('Press enter to continue.')
