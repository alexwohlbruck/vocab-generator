# https://developer.oxforddictionaries.com/documentation
# https://od-api.oxforddictionaries.com/api/v1
# http://docs.python-guide.org/en/latest/scenarios/scrape/

import os
from lxml import html
import requests

words = list()

listLength = int(input('Enter number of words (10) ') or '10')
print(listLength)

for i in range(int(listLength) or 10):
    word = input('Word ' + str(i + 1) + ': ')
    words.append(word)

url = 'https://od-api.oxforddictionaries.com/api/v1/entries/en/' + words[0]
headers = {
    'Accept': 'application/json',
    'app_id': os.environ['OXFORD_APP_ID'],
    'app_key': os.environ['OXFORD_APP_KEY']
}

page = requests.get(url, headers=headers)
tree = html.fromstring(page.content)