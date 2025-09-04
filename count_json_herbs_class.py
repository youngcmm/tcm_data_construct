import json
from collections import Counter

def count_herbs_classes(json_file_path):
    """
    读取JSON数据并计算其中中药的种类
    
    Args:
        json_file_path (str): JSON文件路径
    
    Returns:
        tuple: (总中药种类数, 中药名称集合, 每个处方中中药出现次数统计)
    """
    # 读取JSON数据
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 用于存储所有中药名称
    all_herbs = set()
    # 用于统计中药出现次数
    herbs_counter = Counter()
    
    # 遍历每条数据
    for item in data:
        # 获取处方内容
        prescription = item.get('output', '')
        
        # 提取中药名称
        if prescription.startswith('中药处方：'):
            herbs_str = prescription[5:]  # 去掉"中药处方："前缀
            # 如果全部都是、分割药物，则使用顿号分割
            herbs_list = [herb for herb in herbs_str.split('、') if herb.strip()]
            
            # 添加到集合中（用于统计种类）
            all_herbs.update(herbs_list)
            
            # 统计每个中药出现次数
            herbs_counter.update(herbs_list)
    
    return len(all_herbs), all_herbs, herbs_counter

def main():
    # JSON文件路径
    json_file_path = 'data/processed_data_train.json'
    
    try:
        # 计算中药种类
        total_classes, herbs_set, herbs_count = count_herbs_classes(json_file_path)
        
        # 输出结果
        print(f"中药总种类数: {total_classes}")
        print("\n所有中药名称:")
        for herb in sorted(herbs_set):
            print(f"  {herb}")
        
        print(f"\n中药出现次数统计 (前20种):")
        for herb, count in herbs_count.most_common(20):
            print(f"  {herb}: {count} 次")
        
        # 把herbs_count保存在txt中
        with open('herb_count.txt', 'w', encoding='utf-8') as file:
            for herb, count in sorted(herbs_count.items()):
                file.write(f"{herb}: {count} 次\n")

    except FileNotFoundError:
        print(f"错误: 找不到文件 {json_file_path}")
    except json.JSONDecodeError:
        print(f"错误: 文件 {json_file_path} 不是有效的JSON格式")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()