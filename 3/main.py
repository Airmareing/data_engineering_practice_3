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
		with open(filename, encoding="utf-8") as f:
			text = ""
			for row in f.readlines():
				text += row

			sp = BeautifulSoup(text, 'xml')
			for it in sp.find_all("star"):
				item = {}
				for elem in it.contents:
					if elem.name == "radius":
						item[elem.name] = int(elem.get_text().strip())

					elif elem.name is not None:
						item[elem.name] = elem.get_text().strip()
				items.append(item)

items = sorted(items, key=lambda x: x['age'], reverse=True)
with open("sort.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))

filtered = []
for constellation in items:
	if constellation['constellation'] != 'Близнецы':
		filtered.append(constellation)

st = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['radius'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
st.append(stats)

fr = []

words = [item['name'] for item in items]
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