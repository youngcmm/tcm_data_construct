from helper_function import *
import json
# [!] 必备前提：您需要一个症状关键词列表
SYMPTOM_KEYWORD_LIST = {
    "睡眠差", "难以入睡", "疲乏", "注意力不集中", "齿痕", "舌淡", 
    "苔薄白", "脉弦", "口干", "口苦"
}

def extract_symptoms(text: str, keywords: set) -> set:
    """从文本中提取关键词"""
    found = set()
    for kw in keywords:
        if kw in text:
            found.add(kw)
    return found

QA_TESTSET_OUTPUT = [] # 最终输出的列表 [{"context": c, "question": q, "answer": a, "type": t}, ...]

with open("data/data_cleaned_v7_times2and5_test.json", 'r', encoding='utf-8') as f:
    test_patient_data = json.load(f)
# 1. 遍历 *测试集* 中的每一个患者
for patient_id, visits in test_patient_data.items():
    
    if len(visits) < 2:
        continue # QA测试集必须基于动态病程
        
    visits.sort(key=lambda v: v['第几次问诊'])
    
    # 2. 构建完整的病程上下文 (Context)
    full_context = f"### 患者 {patient_id} 诊疗记录 ###\n\n"
    for v in visits:
        full_context += format_visit_summary(v) + "\n\n"
    
    # 3. 提取每一步的症状和处方，用于生成QA
    symptoms_by_visit = []
    herbs_by_visit = []
    all_symptoms_ever = set()
    
    for v in visits:
        text = v['现病史'] + " " + v['舌苔脉象']
        sym_set = extract_symptoms(text, SYMPTOM_KEYWORD_LIST)
        symptoms_by_visit.append(sym_set)
        all_symptoms_ever.update(sym_set)
        
        herbs_by_visit.append(parse_herbs(v['标准处方药材名称']))
        
    # 4. 循环生成QA对
    
    # [QA类型 1: 症状首现]
    for sym in all_symptoms_ever:
        first_seen_index = -1
        for i, sym_set in enumerate(symptoms_by_visit):
            if sym in sym_set:
                first_seen_index = i
                break
        # 如果在V2或之后才首次出现
        if first_seen_index > 0: 
            question = f"患者在第几次问诊时首次出现‘{sym}’？"
            answer = f"第{first_seen_index + 1}次"
            QA_TESTSET_OUTPUT.append({
                "context": full_context, "question": question, "answer": answer, "type": "Symptom Onset"
            })

    # [QA类型 2: 症状/处方演变]
    for i in range(1, len(visits)):
        V_prev_sym = symptoms_by_visit[i-1]
        V_curr_sym = symptoms_by_visit[i]
        V_prev_herbs = herbs_by_visit[i-1]
        V_curr_herbs = herbs_by_visit[i]
        
        # 2a: 新增症状
        new_symptoms = V_curr_sym - V_prev_sym
        if new_symptoms:
            question = f"与第{i}次问诊相比，第{i+1}次问诊新增的核心症状是什么？"
            answer = format_herbs_to_string(new_symptoms) # 复用函数
            QA_TESTSET_OUTPUT.append({
                "context": full_context, "question": question, "answer": answer, "type": "Symptom Evolution"
            })
            
        # 2b: 新增药物
        new_herbs = V_curr_herbs - V_prev_herbs
        if new_herbs:
            question = f"对比第{i}次处方，第{i+1}次处方中新增了哪些药物？"
            answer = format_herbs_to_string(new_herbs)
            QA_TESTSET_OUTPUT.append({
                "context": full_context, "question": question, "answer": answer, "type": "Prescription Addition"
            })

        # 2c: 移除药物
        removed_herbs = V_prev_herbs - V_curr_herbs
        if removed_herbs:
            question = f"对比第{i}次处方，第{i+1}次处方中去除了哪些药物？"
            answer = format_herbs_to_string(removed_herbs)
            QA_TESTSET_OUTPUT.append({
                "context": full_context, "question": question, "answer": answer, "type": "Prescription Removal"
            })
            
    # [QA类型 3: 症状持续]
    for sym in all_symptoms_ever:
        present_in_all = True
        for sym_set in symptoms_by_visit:
            if sym not in sym_set:
                present_in_all = False
                break
        if present_in_all:
            question = f"‘{sym}’是否在所有{len(visits)}次问诊中都提到了？"
            answer = "是"
            QA_TESTSET_OUTPUT.append({
                "context": full_context, "question": question, "answer": answer, "type": "Symptom Persistence"
            })

# 5. 保存 QA_TESTSET_OUTPUT 到文件
# save_to_jsonl(QA_TESTSET_OUTPUT, "timeline_qa_testset.jsonl")
with open("data/timeline_qa_testset.json", 'w', encoding='utf-8') as f:
    for item in QA_TESTSET_OUTPUT:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")