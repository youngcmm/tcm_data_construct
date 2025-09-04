import json
import random

def augment_data(input_file, output_file):
    """
    对中药处方数据进行增强，将处方中的草药顺序打乱两次，增加两倍数据量
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    augmented_data = []
    
    # 处理每条数据
    for item in data:
        # 添加原始数据
        augmented_data.append(item)
        
        # 获取处方中的草药列表
        prescription_text = item['output']
        # 提取草药部分（去掉"中药处方："前缀）
        herbs_part = prescription_text.replace('中药处方：', '')
        herbs = [herb.strip() for herb in herbs_part.split('、') if herb.strip()]
        herbs[-1] = herbs[-1].replace('。', '')

        # 创建两个打乱顺序的版本
        for _ in range(2):
            # 打乱草药顺序
            shuffled_herbs = herbs.copy()
            random.shuffle(shuffled_herbs)
            
            # 创建新的处方文本
            shuffled_prescription = '中药处方：' + '、'.join(shuffled_herbs) + '。'
            
            # 创建新的数据项
            new_item = item.copy()
            new_item['output'] = shuffled_prescription
            augmented_data.append(new_item)
    
    # 保存增强后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(augmented_data, f, ensure_ascii=False, indent=4)
    
    print(f"原始数据量: {len(data)}")
    print(f"增强后数据量: {len(augmented_data)}")

if __name__ == "__main__":
    input_file = '/Volumes/KINGSTON/code/tcm_data_construct/data/processed_data_train.json'
    output_file = '/Volumes/KINGSTON/code/tcm_data_construct/data/processed_data_train_augment.json'
    random.seed(42)  # 设置随机种子以确保结果可重现
    augment_data(input_file, output_file)