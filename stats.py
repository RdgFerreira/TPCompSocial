import json
from collections import Counter
import matplotlib.pyplot as plt

f = open('memes40001-50000.json')

memes = json.load(f)

print(len(memes))

confirmed = [meme for meme in memes if meme['Status'] == 'Confirmed']
print(len(confirmed))

regions_list = [meme['Region'] for meme in memes if 'Region' in meme.keys()]
regions_distribution = dict(Counter(regions_list))

regions = list(regions_distribution.keys())
number_of_occurrencies = list(regions_distribution.values())

fig = plt.figure(figsize=(10, 5))

rects = plt.bar(regions, number_of_occurrencies, color='tomato',
                width=0.4)

plt.xlabel("Região")
plt.ylabel("Quantidade de memes")
plt.title("Distribuição das regiões")
plt.xticks(rotation=45, ha='right')


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                 '%d' % int(height),
                 ha='center', va='bottom')


autolabel(rects)

plt.show()
