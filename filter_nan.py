#读取sleepy_qa_train.json和sleepy_qa_test.json，将input中主诉：nan，现病史：nan，既往史：nan，四诊：nan的样本去掉
import json
import re

def has_nan_fields(input_text):
    """检查input文本中是否包含nan字段"""
    if not input_text:
        return True
    
    # 检查是否包含这些nan模式
    nan_patterns = [
        r'主诉：nan',
        r'现病史：nan', 
        r'既往史：nan',
        r'舌苔脉象：nan'
    ]
    
    for pattern in nan_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return True
    
    return False

def filter_nan_samples(input_file, output_file):
    """过滤包含nan字段的样本"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"处理文件: {input_file}")
    print(f"原始数据量: {len(data)}")
    
    # 过滤掉包含nan的样本
    filtered_data = []
    removed_count = 0
    
    for item in data:
        input_text = item.get('input', '')
        
        if has_nan_fields(input_text):
            removed_count += 1
        else:
            filtered_data.append(item)
    
    # 保存过滤后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    print(f"移除的样本数: {removed_count}")
    print(f"保留的样本数: {len(filtered_data)}")
    print(f"过滤后数据已保存至: {output_file}")
    print()

if __name__ == "__main__":
    # 处理训练集
    filter_nan_samples('sleepy_qa_train_filtered_bracket_content_with_system_prompt.json', 'sleepy_qa_train_filtered_bracket_content_with_system_prompt_nan.json')
    
    # 处理测试集
    filter_nan_samples('sleepy_qa_test_filtered_bracket_content.json', 'sleepy_qa_test_filtered_bracket_content_nan.json')
    
    print("所有文件处理完成！")
