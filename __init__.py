import json


config = json.load(open(r'./json/config.json', 'rb'))
texts = json.load(open(r'./json/text.json','rb'))

text = {x: texts[x].encode('utf-8').decode() for x in texts}