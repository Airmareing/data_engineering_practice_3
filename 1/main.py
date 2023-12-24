import collections
import json
import os
import re
import zipfile
import pandas as pd
from bs4 import BeautifulSoup


with zipfile.ZipFile('zip_var_42.zip', 'r') as zip:
	zip.extractall()
items = []
for filename in os.listdir():
	if filename.endswith(".html"):
		with open(filename, "r") as f:
			html = f.read()
			sp = BeautifulSoup(html, 'html.parser')
			item = {}
			item['type'] = sp.find('div', {'class': 'chess-wrapper'}).find_all('span')[0].text.split(':')[1].strip()
			item['tournament'] = sp.find('h1', {'class': 'title'}).text.split(':')[1].strip()
			city = sp.find_all("p",attrs={"class": "address-p"})[0].get_text().replace("Город:", "")
			start = city.find("Начало")
			date = city[start:].replace("Начало:", "").strip()
			city = city[:start].strip()
			item["city"] = city
			item["start_date"] = date
			item['num_rounds'] = int(sp.find('span', {'class': 'count'}).text.split(':')[1])
			item['time_control'] = sp.find('span', {'class': 'year'}).text.split(':')[1].strip()
			item['min_rating'] = int(sp.find_all('span')[-1].text.split(':')[1])
			item['rating'] = float(sp.find_all('span')[-3].text.split(':')[1])
			item['views'] = int(sp.find_all("span", string=re.compile("Просмотры:"))[0].getText().split(':')[1].strip())
			items.append(item)

items = sorted(items, key=lambda x: x['rating'], reverse=True)
with open("sort.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))
filtered = []
for it in items:
	if it['views'] < 50000:
		filtered.append(it)

st = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['num_rounds'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
st.append(stats)

fr = []

words = [item['type'] for item in items]
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