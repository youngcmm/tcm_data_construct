import json
from datetime import datetime
from typing import List, Dict, Any

def parse_date(date_str: str) -> datetime:
    """解析日期字符串"""
    return datetime.strptime(date_str, "%Y/%m/%d")

def format_input(patient_records: List[Dict[str, Any]], current_index: int) -> str:
    """
    格式化输入，包括患者基本信息、历史病历和当前病历
    """
    current_record = patient_records[current_index]
    
    # 基本信息
    age = current_record.get("年龄", "")
    input_parts = []
    
    # 添加历史病历信息（如果有的话）
    if current_index > 0:
        history_parts = []
        # 最多显示最近3次历史记录
        start_idx = max(0, current_index - 3)
        for i in range(start_idx, current_index):
            history_record = patient_records[i]
            visit_time = history_record.get("就诊时间", "")
            history_symptoms = []
            if history_record.get("现病史"):
                history_symptoms.append("主诉：" + history_record["现病史"])
            if history_record.get("既往史") and history_record["既往史"].strip() != "":
                history_symptoms.append("既往史：" + history_record["既往史"])
            if history_record.get("舌苔脉象"):
                history_symptoms.append("舌苔脉象：" + history_record["舌苔脉象"])
                
            seq_num = i + 1
            history_parts.append(f"第{seq_num}次就诊（{visit_time}）：" + "；".join(history_symptoms))
        
        input_parts.append("历史就诊记录：" + "；".join(history_parts))
    
    # 当前病历信息
    current_symptoms = []
    if current_record.get("现病史"):
        current_symptoms.append("主诉：" + current_record["现病史"])
    
    if current_record.get("既往史") and current_record["既往史"].strip() != "":
        current_symptoms.append("既往史：" + current_record["既往史"])
        
    if current_record.get("舌苔脉象"):
        current_symptoms.append("舌苔脉象：" + current_record["舌苔脉象"])
    
    input_parts.append("本次就诊：" + "；".join(current_symptoms))
    
    # 构造最终输入
    final_input = "；".join(input_parts)
    if age:
        final_input = f"年龄：{age}岁；{final_input}"
    
    return final_input

def convert_data(input_file: str, output_file: str):
    """
    转换数据格式以适应LLM微调
    """
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 转换后的数据
    converted_data = []
    
    instruction = "请基于患者的主诉、现病史、既往史和舌苔脉象，对病患者给出合适的中药处方。"
    
    # 遍历每个患者
    for patient_id, patient_records in data.items():
        # 按就诊时间排序
        patient_records.sort(key=lambda x: parse_date(x["就诊时间"]))
        
        # 为每个患者的每次就诊生成一条训练数据（只针对有多次就诊记录的患者）
        if len(patient_records) > 1:
            for i, record in enumerate(patient_records):
                # 从第二次就诊开始生成数据，这样才有历史记录可以参考
                if i > 0:
                    # 构造输入
                    input_text = format_input(patient_records, i)
                    
                    # 获取标准处方
                    output_text = "中药处方：" + record.get("标准处方药材名称", "")
                    
                    # 添加到转换后的数据中
                    converted_data.append({
                        "instruction": instruction,
                        "input": input_text,
                        "output": output_text
                    })
    
    # 保存转换后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_file = "data/data_cleaned_v5.json"
    output_file = "data/converted_data_for_finetuning_v2.json"
    convert_data(input_file, output_file)
    print(f"数据转换完成，已保存到 {output_file}")