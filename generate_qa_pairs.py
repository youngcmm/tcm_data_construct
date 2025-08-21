import pandas as pd
import json

# 读取数据
df = pd.read_csv('/Volumes/KINGSTON/code/tcm_data_construct/data/20250718-2-失眠病历数据-仅含有睡眠障碍行的数据.csv')

# 生成问答对
qa_pairs = []

for _, row in df.iterrows():
    # 如果'年龄'、’主诉’、‘现病史’、‘既往史’字段为空，则跳过本行
    if pd.isna(row['年龄']) or pd.isna(row['主诉']) or pd.isna(row['现病史']) or pd.isna(row['既往史']):
        continue
    # 构建input字符串
    input_text = f"年龄：{row['年龄']}，主诉：{row['主诉']}，现病史：{row['现病史']}，既往史：{row['既往史']}，舌苔脉象：{row['体格检查']}"
    
    # 构建output字符串
    output_text = f"""中药处方：{row['标准处方药材名称']}。"""
    
    # 创建问答对
    qa_pair = {
        "system":"你是一位精通传统中医（TCM）的专家，擅长解读患者的主诉、现病史、既往史以及舌苔脉象信息。你的目标是根据所提供的临床信息，制定准确且适宜的中药处方。",
        "instruction": "请基于患者的主诉、现病史、既往史和舌苔脉象，对睡眠慢病患者给出合适的中药处方。",
        "input": input_text,
        "output": output_text
    }
    
    qa_pairs.append(qa_pair)

# 保存为JSON文件
with open('data/sleep_qa.json', 'w', encoding='utf-8') as f:
    json.dump(qa_pairs, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(qa_pairs)} 个问答对，保存至sleep_qa.json")