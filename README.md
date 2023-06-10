# Chatbot Interaction Script

This script allows a particular user to interact with a chatbot that utilizes the memories stored in known knowledge bases (KBs). The chatbot can access and update the KBs specified in the savekb parameter. Additionally, the script enables the chatbot to be aware of user profiles defined in the knownusers parameter. These profiles determine the level of knowledge the chatbot possesses about past conversations and the individuals it has interacted with.

## Usage

To use the script, follow the steps below:

1. Ensure that the required dependencies are installed by running the following command:

   ```
   pip install -r requirements.txt
   ```

2. Set up the necessary configuration files, including:

   - `key_openai.txt`: Provide your OpenAI API key in this file.

3. Configure the script by providing the required command-line arguments:

   - `-user`: Specify the username of the person interacting with the chatbot.
   - `-savechat`: Specify the name of the chat log to be saved and continued from.
   - `-savekb`: Specify the KBs to be updated with new text.
   - `-saveuser`: Specify the user profile to save to.
   - `-knownusers`: Define the profiles that the chatbot is aware of (comma-separated).
   - `-knownkbs`: Specify the KBs the chatbot can access (comma-separated).
   - `-action`: Specify the type of action to be taken from the gpt_actions directory (default: General_Chat).
   - `-lang`: Specify the language the bot should use (default: English).
   - `-persona`: Specify how the bot should behave based on the script in the gpt_personas directory (default: ReflectiveJournalingBot).
   - `-topic`: Set a topic to talk about (default: empty).
   - `-say`: Specify what to say to the bot.

4. Run the script by executing the following command:

   ```
   python chat.py -user Taylor 
      -savechat Taylor-AI-Conversation 
      -savekb Taylor-private 
      -saveuser Taylor-private 
      -knownusers Taylor-private,Taylor-public 
      -knownkbs Taylor-private,Taylor-public 
      -action General_Chat 
      -lang English 
      -persona ReflectiveJournalingBot 
      -topic '' 
      -say "Hello bot! Nice to see you!"
   ```

   The script will initiate the conversation with the chatbot based on the provided arguments and display the chatbot's responses in the terminal.

## Save the relevant details of the conversation:

   The bot will do the following on each run:

   - Chat logs will be saved with the specified name in the savechat parameter.
   - User profiles will be updated with the latest information.
   - Knowledge bases (KBs) will be updated with the new conversation text.

## Features

   This bot contains the ability to form and recall "Memories" from conversations while also forming "Relationships" with user profiles. Fine control of the bots "Memories", "Relationships" and "Knowledge" can be fine-tuned to the context. The power and flexability comes to light when you customize the bot via command line arguments to adapt to conversations and people.
   
   - Create an infinite number of conversations with the bot
   - Seperate out "Memories" the bot has about the conversations
   - Allow the bot to have "Relationships" with other users and share those "Memories" with the current user
   - Allow the user to "Know" a user via the known-profiles argument

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

## Future Features

   -Allow for a -noaction flag to allow the KB and personaly profiles to be updated without the bot being a part of the conversation

## Conclusion
By using this script and configuring the appropriate user profiles and knowledge bases, you can customize the chatbot's level of knowledge about past conversations and the individuals it interacts with.