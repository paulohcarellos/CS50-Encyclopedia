import os
import re
from sys import argv

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/entries/"

files = list(re.sub("\.md$", "", filename)
            for filename in os.listdir(root))

def search(entries, query):
    match = []

    for entry in entries:
        if entry.lower().find(query.lower()) != -1:
            match.append(entry)
    
    return match

print(search(files, argv[1]))