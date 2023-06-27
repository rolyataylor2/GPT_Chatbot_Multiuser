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
import functions_generate as botlib
import functions_kb as kb


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

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('<========================================================>')
    print(center_string(' ', 54))
    print(center_string('~~Welcome to the group chat~~', 54))
    print(center_string('To get started we need some info', 54))
    print(center_string(' ', 54))
    print('<========================================================>')
    lnfeed()

    # Get Bots
    current_bots = []
    bot_input = 'starting'
    while bot_input != '':
        bot_input = input('Enter a bot that will participate in the conversation (blank=finished): ')
        if bot_input == '':
            if len(current_bots) == 0:
                current_bots.append('Spongebob')
                current_bots.append('Patrick')
            break
        else:
            current_bots.append(bot_input)

    # Choose chat
    current_chat = input('Enter the name of the chat: ')
    if current_chat == '':
        current_chat = 'main'
    chatlog = chat.fetch(current_chat,'all_messages',-1)
    chatlength = str(len(chatlog))
    
    chat_itearation = 0
    bot_iteration = 0

    while True:
        # Print system message
        os.system('cls' if os.name == 'nt' else 'clear')
        print('<========================================================>')
        print(center_string('Welcome to the chat!', 54))
        print(center_string(' ', 54))
        print(center_string('Currently Chatting', 54))
        for bot in current_bots:
            print(center_string(bot + ' (' + observer.get_observation('Track_Mood', bot) + ') ' , 54))
        print(center_string(' ', 54))
        print(center_string('Conversation is saved to: ' + current_chat, 54))
        print(center_string('Conversation Length: ' + chatlength, 54))
        print(center_string(' ', 54))
        print('<========================================================>')
        lnfeed()

        # Display chat
        chatlog = chat.fetch(current_chat, 'all_messages', 10)
        for message in chatlog:
            print(format_user_input(message))

        # Iterate through bots
        current_bot = current_bots[bot_iteration]
        bot_iteration += 1
        bot_iteration = bot_iteration % len(current_bots)

        # User input or generate
        current_dialog = input( current_bot + ' Says (...=Autogen, blank=skip): ')
        if current_dialog == '':
            continue
        if current_dialog == '...':
            # Generate a response
            known_kb = []
            known_kb.append( current_chat ) 

            # Chatroom participents
            known_profiles = {}
            for bot in current_bots:
                known_profiles[ bot ] = []
                if "Bot" not in bot:
                    known_profiles[ bot ].append('Emotional_State')
                    known_profiles[ bot ].append('Preferences')
            known_profiles[current_bot].append('persona')

            # Chatroom properties
            extra_tags = {}
            extra_tags['Scene'] = file.open_file('Profiles/' + current_chat + '.location.txt')
            print('\n\nGenerating Repsonse To Chat...')
            current_dialog = botlib.generate(current_bot, current_chat, known_kb, known_profiles)

        #
        #   Add Chat
        #
        print('Adding Repsonse To Chat...')
        chat.add(current_chat, 'user_' + current_bot, current_dialog) # Add user message to personal log
        chat.add(current_chat, 'all_messages', current_bot + ': ' + current_dialog) # Add user message to merged conversation log
        chat.add(current_chat, 'conversation', {'role': 'user', 'content': current_bot + ': ' + current_dialog})

        #
        #   Run observers
        #
        chat_itearation += 1
        chat_itearation = chat_itearation % 5
        if chat_itearation == 0:
            # Code for option 1
            print("Processing... 0")
        elif chat_itearation == 1:
            # Code for option 2
            print("Processing... 1")
            print('    Running Scene Observer...')
            observer.observe('CurrentScene', '', current_chat)
        elif chat_itearation == 2:
            # Code for option 3
            print("Processing... 2")
        elif chat_itearation == 3:
            # Generate Memory
            print("Processing...")
            print('    Creating a memory of the chat...')
            # Make memory
            # latest_conversation = '\n\n'.join( chat.fetch( current_chat, 'all_messages', 10 )).strip()
            # save_kbs = [current_chat]
            # print( kb.update(save_kbs, latest_conversation) )
        elif chat_itearation == 4:
            print("Processing...")
            print('    Running Observers...')
            for bot in current_bots:
                if "Bot" not in bot:
                    observer.observe('Track_Mood', bot, current_chat)
                    observer.observe('Get_Preferences', bot, current_chat)
        else:
            print("Processing... Nothing...")

        input('Prss Enter')
