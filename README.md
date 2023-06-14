# Multi-user Chatbot Project

This project involves the development of a multi-user chatbot using GPT. The chatbot is capable of generating responses, continuing conversations, saving dialogues to chatrooms, and updating profiles, personas, and memories. It provides a versatile platform for interactive communication.

## Save the relevant details of the conversation:

   The bot will do the following on each run:

   - Chat logs will be saved with the specified name in the savechat parameter.
   - User profiles will be updated with the latest information.
   - Knowledge bases (KBs) will be updated with the new conversation text.

## Usage

To use the script, follow the steps below:

1. Ensure that the required dependencies are installed by running the following command:

   ```
   pip install -r requirements.txt
   ```
## Quick Overview

- `chat_add_response.py`: This script allows you to continue a conversation in the chatroom. It saves the dialogues to the specified chat UUID under the identity of the user UUID. It also provides options to add memories, update profiles, and update personas. See the usage instructions below for more details.

- `chatbot_gen.py`: This script generates a bot response to the chatroom and saves it. It also adds memories, updates profiles, and personas. See the usage instructions below for more details.

- `chatbot_gen_response.py`: This script generates a response to the context of a chatroom with the identity of a user. It follows the specified action from the `gpt_actions` directory. This script does not modify any long-term data. See the usage instructions below for more details.

### Common Flags in the scripts

```
  -h, --help        show help message and exit
  -userUUID         User-UUID
  -chatUUID         Chatroom-UUID
  -apikey           Your OpenAI API key. CAUTION: $$$

  -savekbs          Merge Into Additional KBs:
                    Type: Comma-Delimited-List
                    Always updates: $chatUUID,$userUUID

  -savepersona      Merge Additional Personas
                    Type: Comma-Delimited-List
                    Always updates: $userUUID

  -saveprofile      Merge Additional Profiles
                    Type: Comma-Delimited-List
                    Always updates: $userUUID

  -knownusers       Profiles of bot's friends
                    Always has access to: $userUUID
                    If the name contains 'public', the bot will not try to hide details
                    CAUTION: Pure UUIDs are private; bots can't keep secrets

  -knownkbs         Memory Databases for the bot
                    Always has access to: $userUUID
                    CAUTION: These are not kept secret

  -freezekb         Don't write personal KBs
  -freezepersona    Don't write personal persona
  -freezeprofile    Don't write personal profile
  -action           Action to be taken from the gpt_actions directory
  -language         Language that the bot should use. Default is 'English'
  -persona          Override bot's persona using one from the 'gpt_personas' directory
  -topic            Set a topic to talk about
```

## Script Details

### chat_add_response.py

This script allows you to add a response to a chatroom in the multi-user chatbot. It performs the following actions:

- Saves the provided dialogue to the specified chatroom.
- Associates the response with the identity of the user.
- Updates profiles, personas, and memories.

#### Usage

```shell
python3 chat_add_response.py -userUUID [User-UUID] -chatUUID [Chatroom-UUID] -dialog [Dialog to save to the chat] -apikey [Your OpenAI API key]
```

Optional arguments:

- `-savekbs`: Merges into additional knowledge bases. Type: Comma-Delimited-List. Always updates: [Chatroom-UUID],[User-UUID].
- `-savepersona`: Merges additional personas. Type: Comma-Delimited-List. Always updates: [User-UUID].
- `-saveprofile`: Merges additional profiles. Type: Comma-Delimited-List. Always updates: [User-UUID].
- `-freezekb`: Prevents writing personal knowledge bases.
- `-freezepersona`: Prevents writing personal personas.
- `-freezeprofile`: Prevents writing personal profiles.

### chatbot_gen.py

This script generates a bot response for a chatroom in the multi-user chatbot. It performs the following actions:

- Generates a response based on the provided chatroom.
- Saves the response to the chatroom.
- Updates profiles, personas, and memories.

#### Usage

```shell
python3 chatbot_gen.py -userUUID [User-UUID] -chatUUID [Chatroom-UUID] -apikey [Your OpenAI API key]
```

Optional arguments:

- `-savekbs`: Merges into additional knowledge bases. Type: Comma-Delimited-List. Always updates: [Chatroom-UUID],[User-UUID].
- `-savepersona`: Merges additional personas. Type: Comma-Delimited-List. Always updates: [User-UUID].
- `-saveprofile`: Merges additional profiles. Type: Comma-Delimited-List. Always updates: [User-UUID].
- `-knownusers`: Profiles of bot's friends. Always has access to: [User-UUID]. If the name contains 'public,' the bot will not try to hide details.
- `-knownkbs`: Memory databases for the bot. Always has access to: [User-UUID].
- `-freezekb`: Prevents writing personal knowledge bases.
- `-freezepersona`: Prevents writing personal personas.
- `-freezeprofile`: Prevents writing personal profiles.
- `-action`: Action to be taken from the `gpt_actions` directory.
- `-language`: Language that the bot should use. Default is 'English'.
- `-persona`: Overrides the bot's persona using one from the `gpt_personas` directory.
- `-topic`: Sets a topic to talk about.

### chatbot_gen_response.py

This script generates a response to a chatroom conversation in the multi-user chatbot. It performs the following actions:

- Generates a response based on the provided chatroom and user identity.
- Follows the direction specified by the action from the `gpt_actions` directory.
- Does not modify any long-term data.

####

 Usage

```shell
python3 chatbot_gen_response.py -userUUID [User-UUID] -chatUUID [Chatroom-UUID] -apikey [Your OpenAI API key]
```

Optional arguments:

- `-knownusers`: Profiles of bot's friends. Always has access to: [User-UUID]. If the name contains 'public,' the bot will not try to hide details.
- `-knownkbs`: Memory databases for the bot. Always has access to: [User-UUID].
- `-action`: Action to be taken from the `gpt_actions` directory.
- `-language`: Language that the bot should use. Default is 'English'.
- `-persona`: Overrides the bot's persona using one from the `gpt_personas` directory.
- `-topic`: Sets a topic to talk about.

## Features

- Multi-user chatbot system for interactive communication.
- Ability to add responses to chatrooms.
- Generation of bot responses for chatrooms.
- Flexible customization of profiles, personas, and memories.
- Integration with knowledge bases, actions, and topics.
- Easy setup and configuration using command-line arguments.

## Use Case Scenerios
   
   Fine-tuning the bots "Memories", "Relationships" and "Knowledge" can allow for many different use-case scenerios. This is intended to be the back end for a front-end.
   
   Front-end ideas could be:
   
   - Assisted Group Conversations
      - Create a bot that can interject in conversations with relavant information
   - Elaborate on personal interests or self improvement
      - The bot can talk about pretty much anything based on the persona that is loaded
   - Securly share context with friends by creating "Public" KBs
      - Say you are talking with the bot about your birthday coming up, the bot can mention that to your friends in casual conversation
      - You are going to a concert soon, the bot could talk with your friends about it
      - Something has happened to you and you want everyone to know but dont want to message them
   - Make new friends using the KBs to see if your compatible
      - Load up a couple people's profiles and KBs and have the bot say whether the people are compatible???
   
   The GUI should handle permissions between databases, be careful not to share personal KBs with the wrong people

   - You could have a work database that is shared with coworkers
   - You could have a AI ethics database you share with AI ethics boards
   - You can have a relationship database that you share with your significant others
   - You can have a general likes and dislikes database you share with everyone

   Using persona scripts you may be able to have the bot answer questions using your KB and your Profile which may allow for the bot to answer questions on your behalf
   - Maybe a friend can ask the YOU BOT what your favorite food is. The YOU BOT could answer this.


   This bot contains the ability to form and recall "Memories" from conversations while also forming "Relationships" with user profiles. Fine control of the bots "Memories", "Relationships" and "Knowledge" can be fine-tuned to the context. The power and flexability comes to light when you customize the bot via command line arguments to adapt to conversations and people.
   
   - Create an infinite number of conversations with the bot
   - Seperate out "Memories" the bot has about the conversations
   - Allow the bot to have "Relationships" with other users and share those "Memories" with the current user
   - Allow the user to "Know" a user via the known-profiles argument
