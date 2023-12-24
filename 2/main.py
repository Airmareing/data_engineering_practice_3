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
	if filename.endswith(".html"):
		with open(filename, "r") as f:
			text = ""
			for row in f.readlines():
				text += row

			sp = BeautifulSoup(text, 'html.parser')
			products = sp.find_all("div", attrs={'class': 'product-item'})

			for product in products:
				item = dict()
				item['id'] = product.a['data-id']
				item['link'] = product.find_all('a')[1]['href']
				item['img_url'] = product.find_all("img")[0]['src']
				item['title'] = product.find_all("span")[0].get_text().strip()
				item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
				item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())

				props = product.ul.find_all("li")
				for prop in props:
					item[prop['type']] = prop.get_text().strip()

				items.append(item)

items = sorted(items, key=lambda x: x['bonus'], reverse=True)
with open("sort.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))
filtered = []
for it in items:
	if it['price'] < 100000:
		filtered.append(it)

st = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['price'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
st.append(stats)

fr = []

words = [item['title'] for item in items]
col = collections.Counter(words)
fr.append(col)

with open("filter.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(filtered, ensure_ascii=False))

with open("stats.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(st, ensure_ascii=False))

with open("freq.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(fr, ensure_ascii=False))

for filename in os.listdir():
	if filename.endswith(f'.html'):
		os.remove(filename)