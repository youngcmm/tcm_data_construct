import json
import re

def clean_vital_signs(text):
    """清理生命体征数据，如果没有数字记录则删除相应部分"""
    if not text:
        return text
    
    # 匹配T: ℃  P: 次/分  R: 次/分  BP: /mmHg模式
    # 如果没有数字，则删除整个模式
    pattern = r'T\s*:?\s*℃\s*P\s*:?\s*次/分\s*R\s*:?\s*次/分\s*BP\s*:?\s*/mmHg[，,]?'
    
    # 检查是否有数字记录
    vital_match = re.search(r'T\s*:?\s*([\d.]+)?\s*℃\s*P\s*:?\s*([\d.]+)?\s*次/分\s*R\s*:?\s*([\d.]+)?\s*次/分\s*BP\s*:?\s*([\d.]+)?\s*/mmHg', text)
    
    if vital_match:
        # 检查是否所有数字都为空
        t_val, p_val, r_val, bp_val = vital_match.groups()
        if not any([t_val, p_val, r_val, bp_val]):
            # 如果所有数字都为空，删除整个模式
            text = re.sub(pattern, '', text)
    else:
        # 如果没有匹配到完整模式，也删除可能的残留
        text = re.sub(pattern, '', text)
    
    return text

def clean_tongue_pulse(text):
    """清理舌脉诊断，如果没有记录则删除相应部分"""
    if not text:
        return text
    
    # 匹配舌 苔 脉模式
    tongue_pulse_pattern = r'舌苔脉象：舌\s*(.*?)\s*苔\s*(.*?)\s*脉\s*(.*?)(?=[，,T]|$)'
    
    match = re.search(tongue_pulse_pattern, text)
    if match:
        tongue, coating, pulse = match.groups()
        
        # 检查是否都为空或只有空格
        if not tongue.strip() and not coating.strip() and not pulse.strip():
            # 删除整个舌苔脉模式
            text = re.sub(r'舌苔脉象：舌\s*苔\s*脉\s*[，,]?', '', text)
        elif not tongue.strip() or not coating.strip() or not pulse.strip():
            # 部分为空的情况，重构有内容的部分
            parts = []
            if tongue.strip():
                parts.append(f"舌苔脉象：舌{tongue.strip()}")
            if coating.strip():
                parts.append(f"苔{coating.strip()}")
            if pulse.strip():
                parts.append(f"脉{pulse.strip()}")
            
            if parts:
                replacement = '，'.join(parts)
                # 使用字符串替换而不是正则替换
                text = text.replace(match.group(0), replacement)
            else:
                text = re.sub(r'舌苔脉象：舌\s*苔\s*脉\s*[，,]?', '', text)
    
    return text

def clean_herbs(output_text):
    """清理中药处方，排序并去除重复的中草药"""
    if not output_text:
        return output_text
    
    # 匹配中药处方格式
    herb_pattern = r'中药处方：(.*?)[。.]'
    match = re.search(herb_pattern, output_text)
    
    if match:
        herbs_str = match.group(1)
        # 分割中草药
        herbs = re.split(r'[、,，]', herbs_str)
        # 去除空白字符并过滤空字符串
        herbs = [herb.strip() for herb in herbs if herb.strip()]
        # 去重
        unique_herbs = list(set(herbs))
        # unique_herbs = sorted(unique_herbs)
        
        # 重新组合
        cleaned_herbs = '、'.join(unique_herbs)
        
        # 替换原文
        output_text = re.sub(herb_pattern, f'中药处方：{cleaned_herbs}。', output_text)
    
    return output_text

def clean_input_text(input_text):
    """清理输入文本"""
    # 先清理生命体征
    cleaned_text = clean_vital_signs(input_text)
    
    # 再清理舌脉诊断
    cleaned_text = clean_tongue_pulse(cleaned_text)
    
    # 清理多余的逗号和空格
    cleaned_text = re.sub(r'[，,]\s*[，,]+', '，', cleaned_text)  # 多个逗号合并为一个
    cleaned_text = re.sub(r'[，,]\s*$', '', cleaned_text)  # 删除末尾逗号
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # 多个空格合并为一个
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def clean_sleep_qa_data(input_file, output_file):
    """清洗睡眠病历问答对数据"""
    
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据量: {len(data)}")
    
    cleaned_data = []
    cleaned_count = 0
    
    for item in data:
        # 清理input字段
        original_input = item['input']
        cleaned_input = clean_input_text(original_input)
        
        # 清理output字段中的中草药
        original_output = item['output']
        cleaned_output = clean_herbs(original_output)
        
        # 创建清理后的数据项
        cleaned_item = {
            'instruction': item['instruction'],
            'input': cleaned_input,
            'output': cleaned_output
        }
        
        cleaned_data.append(cleaned_item)
        
        # 统计清理情况
        if original_input != cleaned_input or original_output != cleaned_output:
            cleaned_count += 1
    
    # 保存清理后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"清理后数据量: {len(cleaned_data)}")
    print(f"被清理的条目数: {cleaned_count}")
    print(f"清理率: {cleaned_count/len(data)*100:.2f}%")
    print(f"清理后数据已保存至: {output_file}")
    
    # 显示几个清理示例
    print("\n=== 清理示例 ===")
    example_count = 0
    for i, item in enumerate(data):
        original_input = item['input']
        cleaned_input = cleaned_data[i]['input']
        original_output = item['output']
        cleaned_output = cleaned_data[i]['output']
        
        input_changed = original_input != cleaned_input
        output_changed = original_output != cleaned_output
        
        if (input_changed or output_changed) and example_count < 3:
            print(f"\n示例 {example_count + 1}:")
            # if input_changed:
            #     print(f"输入原始: {original_input}")
            #     print(f"输入清理后: {cleaned_input}")
            if output_changed:
                print(f"输出原始: {original_output}")
                print(f"输出清理后: {cleaned_output}")
            example_count += 1

if __name__ == "__main__":
    input_file = '/media/data4/yangcm/tcm_data_construct/data/output_0.json'
    output_file = '/media/data4/yangcm/tcm_data_construct/data/output_0_clean.json'
    
    clean_sleep_qa_data(input_file, output_file)