# Chatbot Interaction Script

This script enables a specific user to interact with a chatbot that leverages the memories stored in known knowledge bases (KBs). The chatbot can access and retrieve information from the KBs specified in the known-kb parameter. Additionally, the chatbot is designed to be aware of user profiles defined in the known-users parameter. These profiles determine the level of knowledge the chatbot possesses about past conversations and the individuals it has interacted with.

## Usage

To utilize the script, follow the steps below:

1. Ensure that the required dependencies are installed by running the following command:

   ```
   pip install -r requirements.txt
   ```

2. Set up the necessary configuration files, including:

   - `key_openai.txt`: Provide your OpenAI API key in this file.
   - `gpt_scripts`: Create a directory named `gpt_scripts` and place the GPT scripts (in .txt format) inside it.

3. Configure the script by providing the required command-line arguments:

   - `--user`: Specify the username of the person making the inquiry.
   - `--save-chat`: Specify the name of the chat log to be saved.
   - `--save-kb`: Specify the KBs to which this conversation should be saved.
   - `--known-users`: Define the profiles the chatbot can access.
   - `--known-kb`: Specify the KBs the chatbot can search.
   - `--action`: Specify the type of action, such as chat, event, code, or something else.
   - `--lang`: Specify the language to use.
   - `--persona`: Specify the personality of the chatbot.
   - `--topic`: Specify the topic of conversation.

   Example usage:
   ```
   python This_Script.py --user=Taylor 
      --save-chat=AI_Taylor_Private 
      --save-kb=AI_Taylor_Private 
      --save-profile=Taylor_Private 
      --known-profiles=Taylor_Private,Taylor_Public,Jack_Public,Thomas_Public,Tiki_Public 
      --known-kb=AI_Taylor_Private,AI_Taylor_Public,AI_Jack_Public,AI_Thomas_public,AI_Tiki_Public 
      --lang=english 
      --AI-Personality=southernbell 
      -lang=english 
      -topic=economic_concerns 
      "What is Jack's favorite food?"
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

By using this script and configuring the appropriate user profiles and knowledge bases, you can customize the chatbot's level of knowledge about past conversations and the individuals it interacts with.