# 统一化json数据中的标准处方药材名称字段的药材名称
import json
from tqdm import tqdm
from extract_herbs import extract_herbs

def clean_json_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in tqdm(data):
        if '中药处方' in item:
            # print(item['中药处方'])
            item['标准处方药材名称'] = extract_herbs(item['中药处方'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    clean_json_data('data/concatenated_tcm_data.json', 'data/concatenated_tcm_data.json')