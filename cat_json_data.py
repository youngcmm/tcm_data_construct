import json
import re
from extract_herbs import create_substitution_dict, extract_herbs

# 读取data/output_0.json文件
def read_data():
    with open('/media/data4/yangcm/tcm_data_construct/data/concatenated_tcm_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 选出病案是否有效的字段其中为是的病案
def filter_valid_cases(data):
    return [item for item in data if item.get('病案是否有效') == '是']

# 将年龄、现病史、既往史拼接起来作为新的json数据的input字段
def create_input_field(item):
    age = item.get('年龄', '')
    present_history = item.get('现病史', '')
    past_history = item.get('既往史', '')
    touge = item.get('舌苔脉象', '')

    # 拼接字段
    input_parts = []
    if age:
        input_parts.append(f"年龄：{age}岁")
    if present_history:
        input_parts.append(f"现病史：{present_history}")
    if past_history:
        input_parts.append(f"既往史：{past_history}")
    if touge:
        input_parts.append(f"舌苔脉象：{touge}")
    return '，'.join(input_parts)

# 将标准化处方药材名称字段的药材名称进行药材名称统一化，参考extract_herbs.py的create_substitution_dict()和extract_herbs()进行药材名称统一化。
def normalize_herbs(herbs_text, substitution_dict):
    return extract_herbs(herbs_text, substitution_dict)

# 主函数
def main():
    # 创建替换字典
    substitution_dict = create_substitution_dict()
    
    # 读取数据
    data = read_data()
    
    # 筛选有效病案
    valid_cases = filter_valid_cases(data)
    
    # 处理数据
    result = []
    for item in valid_cases:
        # 创建input字段
        input_text = create_input_field(item)
        
        # 获取标准化处方药材名称并进行统一化
        herbs_text = item.get('中药处方', '')
        normalized_herbs = normalize_herbs(herbs_text, substitution_dict)
        
        # 只有当有药材时才添加到结果中
        if normalized_herbs:
            new_item = {
                'instruction': '请基于患者的主诉、现病史、既往史和舌苔脉象，对病患者给出合适的中药处方。',
                'input': input_text,
                'output': f'中药处方：{normalized_herbs}'
            }
            result.append(new_item)
    
    # 保存结果
    with open('/media/data4/yangcm/tcm_data_construct/data/concatenated_tcm_data_clean.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成，共处理 {len(result)} 条有效记录")

if __name__ == '__main__':
    main()