from json import load, dump
import re

# do not panic we just using PORTER algorithm from nltk! :D
from nltk.stem import PorterStemmer
porter = PorterStemmer()

import datetime
start = datetime.datetime.now()

# read parsed doc and put it in md (main dictionary)
md_file = open('./parsed_data.json', 'r')
md = load(md_file)
md_file.close()

# stop word file to stop_words
stop_word_file = open('./stopwords.txt', 'r')
stop_words = []
for w in stop_word_file.readlines():
    stop_words.append(w.split('\n')[0])
stop_word_file.close()


def is_stop(char):
    if char in stop_words:
        return True
    else:
        return False

len_md = len(md)

Invert_index = {}
error = 0
# TOKENIZATION & STEMMING
for DID in md:
    print(f'DID: {DID}/{len_md}')
    DID = str(DID)
    # DID = 1
    # print('doc id: ', DID)
    md_text = ''
    md_fav = ''
    try:
        md_text = md[DID]['TEXT']
    except:
        print('Error')
        error += 1
    
    try:
        md_fav = md[DID]['FAVORITE']
    except:
        print('Error')
        error += 1
        

    text = md_text + md_fav
    re_text = re.findall('\w+', text)
    tokenized_text = []

    # tokenization
    for char in re_text:
        char = char.lower()
        if not is_stop(char) and char.isalpha():
            tokenized_text.append(char)

    # print(tokenized_text)

    # STEMMING
    stemmed_words = []
    for w in tokenized_text:
        stemmed_words.append(porter.stem(w))

    for w in stemmed_words:
        if w not in Invert_index:
            Invert_index[w] = {'DocIDs':[DID], 'DocTF': { DID : 1 }, 'DF' : 1 }
        
        else:
            if DID not in Invert_index[w]['DocIDs']:
                Invert_index[w]['DocIDs'].append(DID)
                Invert_index[w]['DocTF'][DID] = 1
                Invert_index[w]['DF'] += 1
            
            elif DID in Invert_index[w]['DocIDs']:
                Invert_index[w]['DocTF'][DID] += 1


print(len(Invert_index))
invert_index_file = open('./invert_index.json', 'w')
dump(Invert_index, invert_index_file)
invert_index_file.close()

print(error)
finish = datetime.datetime.now()

print('Finishing Time:', finish-start)
# print(md['4438'])
# {'file_name': '2007_ford_freestyle',
#  'DATE': '03/28/2009',
#  'AUTHOR': 'jbanks',
#  'TEXT': 'test',
#  'FAVORITE': ''}
