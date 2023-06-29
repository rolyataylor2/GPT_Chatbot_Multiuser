# Multi-user Chatbot Project

This project involves the development of a multi-user chatbot using GPT. The chatbot is capable of generating responses, continuing conversations, saving dialogues to chatrooms, and updating profiles, personas, and memories. It provides a versatile platform for interactive communication.

## Save the relevant details of the conversation:

   The bot will do the following on each run:

   - Chat logs will be saved with the specified name in the savechat parameter.
   - User profiles will be updated with the latest information.
   - Knowledge bases (KBs) will be updated with the new conversation text.

## Usage

To use the script, follow the steps below:

1. Clone the repo

2. Ensure that the required dependencies are installed by running the following command:

   ```
   pip install -r requirements.txt
   ``` 
3. Fill in your api key in the text file.


## Quick Overview

- `converse.py`: This script is a user interface for the following scripts, run this to engage in a full chat interface with bots

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
