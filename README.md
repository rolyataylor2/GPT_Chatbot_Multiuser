# Chatbot Interaction Script

This script enables a specific user to interact with a chatbot that leverages the memories stored in known knowledge bases (KBs). The chatbot can access and retrieve information from the KBs specified in the known-kb parameter. Additionally, the chatbot is designed to be aware of user profiles defined in the known-users parameter. These profiles determine the level of knowledge the chatbot possesses about past conversations and the individuals it has interacted with.

## This does not work yet

## Usage

To utilize the script, follow the steps below:

1. Ensure that the required dependencies are installed by running the following command:

   ```
   pip install -r requirements.txt
   ```

2. Set up the necessary configuration files, including:

   - `key_openai.txt`: Provide your OpenAI API key in this file.

3. Configure the script by providing the required command-line arguments:

   - `--user`: Specify the username of the person making the inquiry.
   - `--save-chat`: Specify the name of the chat log to be saved.
   - `--save-kb`: Specify the KBs to which this conversation should be saved.
   - `--known-users`: Define the profiles the chatbot can access.
   - `--known-kb`: Specify the KBs the chatbot can search.
   - `--action`: Specify the type of action dialog for the bot to be loaded from
   - `--lang`: Specify the language to use.
   - `--persona`: Specify the personality of the chatbot.
   - `--topic`: Specify the topic of conversation.

   Example usage:
   ```
   python This_Script.py --user=Taylor 
      --save-chat=AI_Taylor_Private 
      --save-kb=AI_Taylor_Private 
      --save-profile=Taylor_Private 
      --known-profiles=Taylor_Private,Taylor_Public
      --known-kb=AI_Taylor_Private,AI_Taylor_Public
      --lang=english 
      --AI-Personality=ReflectiveJournalingBot 
      --lang=english 
      --topic=economic_concerns 
      --action=general_chat
      "Hello my name is Taylor"
   ```

4. Run the script by executing the following command:

   ```
   python This_Script.py
   ```

   The script will execute the conversation with the chatbot based on the provided arguments and display the chatbot's responses in the terminal.

5. Save the relevant details of the conversation:

   - Chat logs will be saved based on the provided `--save-chat` argument.
   - User profiles will be updated with the latest notes.
   - Long-term memory (KBs) will be updated with the latest conversation.

   Additionally, the Chroma Database will be persisted to save all the conversation details.

6. Features

   What can you do with it?
   
   - Create an infinite number of conversations with the bot
   - Seperate out "Memories" the bot has about the conversations
   - Allow the bot to have "Relationships" with other users and share those "Memories" with the current user
   - Allow the user to "Know" a user via the known-profiles argument

7. Use Case Scenerios

   - Create a bot that can interject in conversations about past conversations
   - The bot can talk about things that you are interested in with friends
      - Say you are talking with the bot about your birthday coming up, the bot can mention that to your friends in casual conversation
      - You are going to a concert soon, the bot could talk with your friends about it
      - Something has happened to you and you want everyone to know but dont want to message them
      - The bot could include your public KB's and make new friends for you
   - The GUI should handle permissions between databases, Maybe allow the user to share certain databases with others
      - You could have a work database that is shared with coworkers
      - You could have a AI ethics database you share with AI ethics boards
      - You can have a relationship database that you share with your significant others
      - You can have a general likes and dislikes database you share with everyone
   - Have a bot make decisions on your behalf
      - Creating custom GPT_personalities would allow for the bot to use your KB and profile to chat on your behalf
   - Custom GPT_Personalities for controlling devices
      - Create a persona that can issue commands, This persona knows you through your KB and profile to allow it to customize those commands

By using this script and configuring the appropriate user profiles and knowledge bases, you can customize the chatbot's level of knowledge about past conversations and the individuals it interacts with.