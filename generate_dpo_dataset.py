import random
from helper_function import *
import json

# [!] 占位符：您需要加载一个已有的静态基线模型
# static_model = load_model("SuiZheng-Static") 

DPO_TRIPLETS_OUTPUT = [] # 最终输出的列表 [{"prompt": p, "chosen": c, "rejected": r}, ...]

# filter 2-5次访问的患者
# with open("data/data_cleaned_v7.json", 'r', encoding='utf-8') as f:
#     data = json.load(f)

# training_patient_data = {}
# for id, visits in data.items():
#     if 2 <= len(visits) <= 5:
#         training_patient_data[id] = visits
# # 从training_patient_data中随机选出 1000 个患者作为测试
# random_patient_ids = random.sample(list(training_patient_data.keys()), 1000)
# testing_ptient_data = {id: visits for id, visits in data.items() if id in random_patient_ids}

# # 剩余的患者作为训练数据
# training_patient_data = {id: visits for id, visits in training_patient_data.items() if id not in random_patient_ids}

# with open("data/data_cleaned_v7_times2and5_train.json", 'w', encoding='utf-8') as f:
#     json.dump(training_patient_data, f, ensure_ascii=False, indent=2)

# with open("data/data_cleaned_v7_times2and5_test.json", 'w', encoding='utf-8') as f:
#     json.dump(testing_ptient_data, f, ensure_ascii=False, indent=2)
with open("data/data_cleaned_v7_times2and5_train.json", 'r', encoding='utf-8') as f:
    training_patient_data = json.load(f)

# 1. 遍历训练数据中的每一个患者
for patient_id, visits in training_patient_data.items():
    
    # 必须至少有2次就诊
    if len(visits) < 2:
        continue
        
    # 确保按就诊次序排序
    visits.sort(key=lambda v: v['第几次问诊'])
    
    historical_summary_text = ""
    
    # 2. 从 V2 开始，遍历每一次复诊
    for i in range(1, len(visits)):
        V_prev = visits[i-1] # V(n-1)
        V_curr = visits[i]   # V(n)
        
        # 3. 构建历史病历 (作为 Prompt 的一部分)
        historical_summary_text += format_visit_summary(V_prev) + "\n---\n"
        
        # 4. 构建 Prompt (P)
        prompt = f"""
        ### 历史就诊记录 ###
        {historical_summary_text.strip()}
        
        ### 本次（第{V_curr['第几次问诊']}次）就诊 ###
        就诊时间: {V_curr['就诊时间']}
        主诉/病史: {V_curr['现病史']}
        舌脉: {V_curr['舌苔脉象']}
        ---
        请根据本次就诊的病史，并参考历史诊疗过程，给出本次的处方：
        """
        
        # 5. 构建 Chosen (C) - 黄金标准
        chosen_prescription_str = V_curr['标准处方药材名称']
        
        # 6. 自动化构建 Rejected (R) 列表
        rejected_prescriptions = []
        
        # [策略 1: R_Static] (静态模型生成)
        # 仅使用V_curr信息生成一个“静态”处方
        static_prompt = f"主诉: {V_curr['现病史']}, 舌脉: {V_curr['舌苔脉象']}. 请开处方："
        # R_Static = static_model.generate(static_prompt) # 假设模型输出标准药材字符串
        # rejected_prescriptions.append(R_Static)
        
        # [策略 2: R_Inertia] (处方惯性/惰性)
        # 直接复用上一次的处方
        R_Inertia = V_prev['标准处方药材名称']
        rejected_prescriptions.append(R_Inertia)
        
        # [策略 3: R_Mal-adjustment] (错误调整 - 规则生成)
        herbs_prev = parse_herbs(V_prev['标准处方药材名称'])
        herbs_chosen = parse_herbs(chosen_prescription_str)
        
        herbs_that_should_be_removed = herbs_prev - herbs_chosen
        herbs_that_should_be_added = herbs_chosen - herbs_prev
        
        # 3a: 模拟“忘记删除药物”
        if len(herbs_that_should_be_removed) > 0:
            herb_to_wrongly_keep = random.choice(list(herbs_that_should_be_removed))
            R_FailureToRemove_Set = herbs_chosen | {herb_to_wrongly_keep}
            rejected_prescriptions.append(format_herbs_to_string(R_FailureToRemove_Set))

        # 3b: 模拟“忘记添加新药”
        if len(herbs_that_should_be_added) > 0:
            herb_to_wrongly_omit = random.choice(list(herbs_that_should_be_added))
            R_Omission_Set = herbs_chosen - {herb_to_wrongly_omit}
            rejected_prescriptions.append(format_herbs_to_string(R_Omission_Set))
            
        # 7. 组合并写入最终列表
        for r in rejected_prescriptions:
            # 确保 C 和 R 不完全相同
            if r != chosen_prescription_str and r is not None:
                DPO_TRIPLETS_OUTPUT.append({
                    "prompt": prompt,
                    "chosen": chosen_prescription_str,
                    "rejected": r
                })

# 8. 保存 DPO_TRIPLETS_OUTPUT 到文件 (e.g., JSONL)
# save_to_jsonl(DPO_TRIPLETS_OUTPUT, "dpo_dataset.jsonl")
with open("data/timeline_dpo_train.json", 'w', encoding='utf-8') as f:
    for triplet in DPO_TRIPLETS_OUTPUT:
        json.dump(triplet, f, ensure_ascii=False)
        f.write("\n")