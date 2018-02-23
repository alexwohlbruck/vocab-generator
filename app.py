# https://developer.oxforddictionaries.com/documentation

import os
import random
import datetime
import json
import requests

doc_name = (input('Enter document name: ') or 'Vocab')
name = (input('Enter your name: ') or 'Alex')
date = datetime.datetime.now()
listLength = int(input('Enter number of words (10): ') or '10')

words = list()

for i in range(int(listLength) or 10):
    word = input('Word ' + str(i + 1) + ': ')
    words.append(word)
    
base_url = 'https://od-api.oxforddictionaries.com/api/v1/'
headers = {
    'Accept': 'application/json',
    'app_id': os.environ['OXFORD_APP_ID'],
    'app_key': os.environ['OXFORD_APP_KEY']
}

    
def get_dictionary_url(endpoint, word):
    return {
        'definition': base_url + 'entries/en/' + word,
        'thesaurus': base_url + 'entries/en/' + word + '/synonyms',
        'sentence': base_url + 'entries/en/' + word + '/sentences'
    }[endpoint]


def dictionary(endpoint, word):
    r = requests.get(get_dictionary_url(endpoint, word), headers=headers)
    
    if (r.status_code == 200):
        return r.json()
    else:
        print ('Could not get ' + endpoint + ' entry for ' + word)
        print (r)
        return None
    
results = list(map(lambda word: {
    'definition': dictionary('definition', word),
    'thesaurus': dictionary('thesaurus', word),
    'sentence': dictionary('sentence', word)
}, words))
    
f = open('output.txt', 'w')

# Output title, name, and date
f.write(' – '.join([doc_name, name, date.strftime('%b %d, %Y')]) + '\n\n')

for index, word in enumerate(results):
    
    text = word['definition']['results'][0]['word']
    definition = word['definition']['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    partOfSpeech = word['definition']['results'][0]['lexicalEntries'][0]['lexicalCategory']
    sentences = list(map((lambda d: d['text']), word['sentence']['results'][0]['lexicalEntries'][0]['sentences']))
    
    if word['thesaurus'] is None:
        synonyms = []
    else:
        synonyms = list(map((lambda d: d['text']), word['thesaurus']['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms'][0:3]))
    
    # Output word + pos
    f.write(str(index + 1) + '. ' + text.capitalize() + ' (' + partOfSpeech + ')' + '\n')
    
    # Output definition
    f.write(definition + '\n')
    
    # Output synonyms
    if word['thesaurus'] is not None:
        f.write(', '.join(synonyms) + '\n')
    
    # Output sentence
    f.write('"' + random.choice(sentences) + '"' + '\n\n')
    
f.close()