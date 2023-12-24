import collections
import json
import os
import zipfile

import pandas as pd
from bs4 import BeautifulSoup

with zipfile.ZipFile('zip_var_42.zip', 'r') as zip:
	zip.extractall()
items = []
for filename in os.listdir():
	if filename.endswith(".xml"):
		with open(filename, "r") as f:
			text = ""
			for row in f.readlines():
				text += row

			sp = BeautifulSoup(text, 'xml')
			for clothing in sp.find_all("clothing"):
				item = dict()
				for elem in clothing.contents:
					if elem.name is None:
						continue
					elif elem.name == "price" or elem.name == "reviews":
						item[elem.name] = int(elem.get_text().strip())
					elif elem.name == "price" or elem.name == "rating":
						item[elem.name] = float(elem.get_text().strip())
					elif elem.name == "new":
						item[elem.name] = elem.get_text().strip() == "+"
					elif elem.name == "exclusive" or elem.name == "sporty":
						item[elem.name] = elem.get_text().strip() == "yes"
					else:
						item[elem.name] = elem.get_text().strip()

				items.append(item)

items = sorted(items, key=lambda x: x['rating'], reverse=True)
with open("sort.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))

filtered = []
for color in items:
	if color['material'] != 'Шелк':
		filtered.append(color)

st = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['price'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
st.append(stats)

fr = []

words = [item['category'] for item in items]
col = collections.Counter(words)
fr.append(col)

with open("filter.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(filtered, ensure_ascii=False))

with open("stats.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(st, ensure_ascii=False))

with open("freq.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(fr, ensure_ascii=False))

for filename in os.listdir():
	if filename.endswith(f'.xml'):
		os.remove(filename)