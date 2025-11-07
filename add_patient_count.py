# 加载data_cleaned_v4.json数据，统计同一个病患id的个数，并根据就诊时间排序，加入第几次问诊的字段。
import json
from tqdm import tqdm

def add_patient_count(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 使用字典按患者ID分组数据，提高查找效率
    patient_data_dict = {}
    for item in data:
        patient_id = item['患者个人id']
        if patient_id not in patient_data_dict:
            patient_data_dict[patient_id] = []
        patient_data_dict[patient_id].append(item)
    
    print(f"病患id个数: {len(patient_data_dict)}")

    # 针对同一个病患id的问诊，根据就诊时间字段排序，计算第几次问诊，并加入第几次问诊的字段。
    count_num_plus_zero = 1 # 统计数量大于1的病患id个数
    for patient_id, patient_data in tqdm(patient_data_dict.items()):
        # 按就诊时间排序
        patient_data.sort(key=lambda x: x['就诊时间'])
        
        # 添加问诊次数信息
        count = len(patient_data)
        for i, item in enumerate(patient_data):
            item['第几次问诊'] = i + 1
            item['总共问诊次数'] = count
        if count > 1:
            count_num_plus_zero += 1
    print(f"数量大于1的病患id个数: {count_num_plus_zero}")
    # 保存patient_data_dict数据
    with open('./data/data_cleaned_v7.json', 'w', encoding='utf-8') as f:
            json.dump(patient_data_dict, f, ensure_ascii=False, indent=4)

add_patient_count('./data/data_cleaned_v6.json')