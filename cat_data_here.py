import json
import os
import glob
# 合并所有json文件到本地data目录下
def cat_json_files(source_dir, output_file):
    """
    将指定目录下的所有JSON文件合并为一个文件
    """
    # 获取所有JSON文件
    json_files = glob.glob(os.path.join(source_dir, "*.json"))
    print(f"找到 {len(json_files)} 个JSON文件")
    
    # 存储所有数据
    all_data = []
    
    # 读取每个JSON文件并合并数据
    for i, file_path in enumerate(json_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 如果data是一个列表，扩展all_data
                if isinstance(data, list):
                    all_data.extend(data)
                # 如果data是一个字典，添加到all_data中
                else:
                    all_data.append(data)
            if (i + 1) % 100 == 0:
                print(f"已处理 {i + 1} 个文件")
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
    
    # 将合并后的数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"合并完成，总共 {len(all_data)} 条记录，保存至 {output_file}")

if __name__ == "__main__":
    source_directory = "/media/data3/huangjunj/TCM_dataset/cleaned"
    output_file = "data/concatenated_tcm_data.json"
    cat_json_files(source_directory, output_file)