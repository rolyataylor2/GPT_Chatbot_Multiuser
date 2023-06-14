#
# Help screen and get arguments
#

import argparse
from argparse import RawTextHelpFormatter
description = 'Multi-user Chatbot using GPT - Add a memory to a KB.\n\n'
description += 'How to add a memory:\n'
description += ' - Provide the kbname and the memory text\n'
description += ' - To append the memory to another memory use the context as a search\n'
description += '      !!! Memories that exceed 1000 words will be rejected !!!\n\n'
description += 'Why add a memory:\n'
description += ' - Adding memories to a KB can allow for artificial knowledge to be added to a bot.\n'
description += ' - Bots can be given "Lives" by incorporating memories of events that did not take place.\n'
description += ' - Bots can be given technical skills by including documentation to their memories\n\n'
description += 'How DBs are tagged:\n'
description += ' - Default Private KBs are named after the botUUID\n'
description += ' - Bot~Human Private KBs are named as botUUID + "-" + userUUID\n'
description += ' - Any other DB can be named in any way. Example: Public-Plumbing-Skill, Public-Relationship-Skills\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)

# Required arguments
parser.add_argument("-kbname", metavar='Knowledge-Base', required=True, help="KB to add memory too")
parser.add_argument("-memory", metavar='Memory-Text', required=True, help="The memory to add")
parser.add_argument("-context", metavar='Context', required=False, help="Context for the memory")
args = parser.parse_args()

#
#   Imports
#
import chromadb
from chromadb.config import Settings
from uuid import uuid4
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


#
# KB management
#   filename - What name to store the database under
#
knowledgeBasesDirectory = 'chromadb'
chroma_client = chromadb.Client(Settings(persist_directory=knowledgeBasesDirectory,chroma_db_impl="duckdb+parquet",))
def KBSearch(profile, context, limit_results=1):
    # Fetch the right collection
    collection = chroma_client.get_or_create_collection(name=profile)
    if collection.count() == 0:
        return "No new KB article could be created based on the given chat logs."

    # Search Database, return results
    results = collection.query(query_texts=[context], n_results=limit_results)
    kb = results['documents'][0][0]
    kb_id = results['ids'][0][0]
    return kb, kb_id
def KBAdd(profile, memory, kb_id=-1):
    collection = chroma_client.get_or_create_collection(name=profile)
    memory = memory.strip()
    if kb_id == -1:
        collection.add(ids=[str(uuid4())],documents=[memory])
    else:
        collection.update(ids=[kb_id],documents=[memory])

if __name__ == '__main__':
    # UUID of user and bot, bots are treated as users
    kb_name = args.kbname
    memory_text = args.memory
    memory_context = args.context

    # 
    #   Search Long Term memory and pull relavant memories
    #
    kb_id = -1
    if memory_context:
        kb_text, kb_id = KBSearch(kb_name, memory_context, 1)
        if kb_text == "No new KB article could be created based on the given chat logs.":
            kb_id = -1
    if len(memory_text.split(' ')) < 1000:
        KBAdd(kb_name, memory_text, kb_id) # Update bots personal memories
        chroma_client.persist()
        print('Installed Memory Into Knowledge Base')
    else:
        print('Memory has been rejected due to length')
    

    
