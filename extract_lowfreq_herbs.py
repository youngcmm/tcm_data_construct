import json
from collections import Counter, OrderedDict
import pandas as pd
from tqdm import tqdm

with open('./data/data_cleaned_v3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lst = []
for _, item in enumerate(data):
    herbs = item["标准处方药材名称"].split("、")
    lst += herbs

counter = Counter(lst)
seen = set(lst)
freq = dict()
seldom_herbs = []
for _, i in enumerate(seen):
    freq[i] = counter[i]
    if counter[i] <= 321: seldom_herbs.append(i)       # 筛选少量组方药 出现频次 <= 321

new_data = []                                          # 去掉含有少量组方药的病案
for item in tqdm(data):
    herbs = item["标准处方药材名称"].split("、")
    has_common = bool(set(herbs) & set(seldom_herbs))
    if not has_common:
        new_data.append(item)
print(len(new_data))
with open('data/v4.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

# sorted_freq = OrderedDict(sorted(freq.items(), key=lambda item: item[1]))
# with open('./freq_1.json', 'w', encoding='utf-8') as f:
#     json.dump(sorted_freq, f, ensure_ascii=False, indent=2)
