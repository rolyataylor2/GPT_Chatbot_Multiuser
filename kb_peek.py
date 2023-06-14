import argparse
from argparse import RawTextHelpFormatter
description = 'Multi-user Chatbot using GPT - View a KB.\n\n'
parser = argparse.ArgumentParser(description=description, usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)

# Required arguments
parser.add_argument("-kbname", metavar='Knowledge-Base', required=True, help="KB to add memory too")
args = parser.parse_args()

import chromadb
from chromadb.config import Settings
from pprint import pprint as pp

persist_directory = "chromadb"
chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
collection = chroma_client.get_or_create_collection(name=args.kbname)

print('KB presently has %s entries' % collection.count())
print('\n\nBelow are the top 10 entries:')
results = collection.peek()
pp(results)