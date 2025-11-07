import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import os

# 检查是否有GPU可用
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

def load_model(model_path):
    """
    Load the model and tokenizer
    """
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    # 对于大模型，使用device_map="auto"自动分配到可用设备
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype="auto",
        trust_remote_code=True,
        device_map="auto"
    )
    model.eval()
    print("Model loaded successfully.")
    return model, tokenizer

def extract_tcm_features_with_llm(case_data, model, tokenizer):
    """
    Use LLM to extract key symptoms, tongue conditions, pulse conditions, and corresponding herbs
    """
    prompt = f"""根据提供的中医病案信息，提取关键症状、舌象、脉象以及治疗这些症状的关键药材。

病案信息：
现病史：{case_data.get('现病史', '')}
既往史：{case_data.get('既往史', '')}
舌苔脉象：{case_data.get('舌苔脉象', '')}
标准处方药材名称：{case_data.get('标准处方药材名称', '')}

请以以下JSON格式输出：
{{
    "key_symptoms": ["症状1", "症状2", ...],
    "tongue_condition": "舌象描述",
    "pulse_condition": "脉象描述",
    "key_herbs": {{
        "药材名1": "针对的关键症状",
        "药材名2": "针对的关键症状"
    }}
}}

请确保：
1. key_symptoms只包含现病史以及舌苔脉象中具体的症状，如"失眠"、"口干、苔黄、纳差"等
2. tongue_condition是舌象描述，如"舌淡苔薄白"
3. pulse_condition是脉象描述，如"脉弦"
4. key_herbs是药材名到其作用的映射，只包含标准处方药材名称中的药材

只输出JSON，不要包含其他文字。"""

    # 构造完整的对话消息
    messages = [
        {"role": "system", "content": "你是一位专业的中医数据分析专家。"},
        {"role": "user", "content": prompt}
    ]
    
    # 应用聊天模板
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # 编码输入
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    try:
        # 生成响应
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=1000,
            temperature=0.3,
            do_sample=True
        )
        
        # 去除输入部分，只保留生成的部分
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        # 解码生成的文本
        result_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # 清理结果文本，只保留JSON部分
        # 找到第一个{和最后一个}之间的内容
        start = result_text.find('{')
        end = result_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_text = result_text[start:end+1]
            # 尝试解析JSON
            return json.loads(json_text)
        else:
            print(f"Could not extract valid JSON from response: {result_text}")
            return None
            
    except Exception as e:
        print(f"Error processing case: {e}")
        return None

def load_checkpoint(output_file):
    """
    Load existing results from output file as checkpoint
    """
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            print(f"Loaded checkpoint with {len(existing_data)} records")
            return existing_data
        except Exception as e:
            print(f"Failed to load checkpoint: {e}")
            return []
    return []

def process_tcm_data(input_file, output_file, batch_size=4, resume_from=0, model_path="/media/data3/huangjunj/pretrained_models/FreedomIntelligence/ShizhenGPT-32B-LLM"):
    """
    Process TCM data file and extract features using LLM
    """
    # Load model
    model, tokenizer = load_model(model_path)
    
    # Read input data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total cases in input: {len(data)}")
    
    # Load existing results if any (checkpoint)
    results = load_checkpoint(output_file)
    processed_count = len(results)
    
    # If resuming, skip already processed cases
    start_index = max(processed_count, resume_from)
    if start_index > 0:
        print(f"Resuming from sample {start_index + 1}")
    
    # Process each case
    for i in range(start_index, len(data)):
        case = data[i]
        print(f"Processing case {i+1}/{len(data)}")
        extracted_features = extract_tcm_features_with_llm(case, model, tokenizer)
        
        # Create a new entry with original data and extracted features
        if extracted_features:
            # Merge original case data with extracted features
            merged_entry = case.copy()  # Start with original data
            merged_entry.update(extracted_features)  # Add extracted features
            results.append(merged_entry)
        else:
            # If extraction failed, keep original data
            results.append(case)
        
        # Save batch results every batch_size cases
        if (len(results) % batch_size == 0) or (i + 1 == len(data)):
            # Save results incrementally
            save_results(results, output_file)
            print(f"Saved {len(results)} records to {output_file}")
    
    # Save final results
    save_results(results, output_file)
    print(f"Processing complete. Results saved to {output_file}")
    
    # 清理模型以释放内存
    del model
    del tokenizer
    torch.cuda.empty_cache()

def save_results(results, output_file):
    """
    Save results to JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    input_file = "data/data_cleaned_v4.json"
    output_file = "data/data_cleaned_v4_extract_features.json"
    
    # 确保data目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Resume from sample 5061 (0-indexed, so it's actually 5060)
    process_tcm_data(input_file, output_file, resume_from=5063)

if __name__ == "__main__":
    main()