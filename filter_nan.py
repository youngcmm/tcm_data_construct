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

def chinese_char_count(text):
    """计算文本中中文字符的数量"""
    if not text:
        return 0
    # 使用正则表达式匹配中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)

def filter_nan_samples(input_file, output_file):
    """过滤包含nan字段的样本"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"处理文件: {input_file}")
    print(f"原始数据量: {len(data)}")
    
    # 过滤掉包含nan的样本
    filtered_data = []
    removed_count = 0
    nan_removed = 0
    input_length_removed = 0
    output_length_removed = 0
    
    for item in data:
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # 检查是否包含nan字段
        if has_nan_fields(input_text):
            nan_removed += 1
            removed_count += 1
            continue
        
        # 检查input长度是否符合要求(41-230个中文字符)
        input_chinese_count = chinese_char_count(input_text)
        if input_chinese_count < 41 or input_chinese_count > 230:
            input_length_removed += 1
            removed_count += 1
            continue
        
        # 检查output长度是否符合要求(至少14个中文字符)
        output_chinese_count = chinese_char_count(output_text)
        if output_chinese_count < 14:
            output_length_removed += 1
            removed_count += 1
            continue
            
        filtered_data.append(item)
    
    # 保存过滤后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    print(f"移除的样本数: {removed_count}")
    print(f"  - nan字段移除: {nan_removed}")
    print(f"  - input长度不符合要求移除: {input_length_removed}")
    print(f"  - output长度不符合要求移除: {output_length_removed}")
    print(f"保留的样本数: {len(filtered_data)}")
    print(f"过滤后数据已保存至: {output_file}")
    print()

if __name__ == "__main__":
    
    filter_nan_samples('/Volumes/KINGSTON/code/tcm_data_construct/data/sleep_qa_clean.json', '/Volumes/KINGSTON/code/tcm_data_construct/data/sleep_qa_clean_nan.json')
    
    print("所有文件处理完成！")