import json

texts = json.load(open('text.json','rb'))

text = {x: texts[x].encode('utf-8').decode() for x in texts}