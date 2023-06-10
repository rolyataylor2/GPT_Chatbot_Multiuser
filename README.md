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
   - `gpt_scripts`: Create a directory named `gpt_scripts` and place the GPT scripts (in .txt format) inside it.

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

   Example usage:
   ```
   python chat.py -user Taylor 
      -savechat Taylor-AI-Conversation 
      -savekb Taylor-private 
      -saveuser Taylor-private 
      -knownusers Taylor-private,Taylor-public 
      -knownkbs kbone,kbtwo,kbthree 
      -action General_Chat 
      -lang English 
      -persona ReflectiveJournalingBot 
      -topic '' 
      -say "Hello bot! Nice to see you!"
   ```

4. Run the script by executing the following command:

   ```
   python This_Script.py
   ```

   The script will initiate the conversation with the chatbot based on the provided arguments and display the chatbot's responses in the terminal.

5. Save the relevant details of the conversation:

   - Chat logs will be saved with the specified name in the savechat parameter.
   - User profiles will be updated with the latest information.
   - Knowledge bases (KBs) will be updated with the new conversation text.

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