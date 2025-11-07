# 去掉/media/data4/yangcm/tcm_data_construct/data/output_0_cleaned.json中病案是否有效字段为否的数据，然后存储在新的文件中
import json
from tqdm import tqdm
def main(input_file, output_file):
    input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3.json'
    output_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        valid_data = [item for item in data if item['病案是否有效'] == '是']
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(valid_data, f, ensure_ascii=False, indent=4)
            print(f"原始数据量: {len(data)}")
            print(f"有效数据量: {len(valid_data)}")
            print(f"保存文件成功: {output_file}")
            return

# 统计'/media/data4/yangcm/tcm_data_construct/data/concatenated_tcm_data_valid.json'的标准处方药材名称字段中出现过的药材的数量
def count_unique_medicines(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json',
                            output_file = '/media/data4/yangcm/tcm_data_construct/data/herbs.json'):
    input_file = input_file
    medicine_counts = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"数据量: {len(data)}")
        for item in data:
            medicines = item['标准处方药材名称']
            # 这里需要对medicines使用、进行分割处理
            medicines = medicines.split('、')
            for medicine in medicines:
                if medicine not in medicine_counts:
                    medicine_counts[medicine] = 1
                else:
                    medicine_counts[medicine] += 1
    data = sorted(medicine_counts.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return medicine_counts

# 统计'herbs.json'中药材出现的次数低于322次的草药名称
def count_low_frequency_medicines(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json',
                                output_file = '/media/data4/yangcm/tcm_data_construct/data/herbs_list_name_low_322.json'):
    medicine_counts = count_unique_medicines(input_file)
    print(medicine_counts)
    low_frequency_medicines = [medicine for medicine, count in medicine_counts.items() if count < 322]
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(low_frequency_medicines, f, ensure_ascii=False, indent=4)
    return low_frequency_medicines

# 读取/media/data4/yangcm/tcm_data_construct/data/herbs_list_name_low_336.json，同时读取/media/data4/yangcm/tcm_data_construct/data/concatenated_tcm_data_valid.json
# 如果存在药材名称在herbs_list_name_low_336,则将该样本删掉
def remove_low_frequency_medicines(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json', 
            output_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid_remove_low.json',
            herbs_list_file = '/media/data4/yangcm/tcm_data_construct/data/herbs_list_name_low_322.json'):
    input_file = input_file
    output_file = output_file
    herbs_list_file = herbs_list_file
    herbs_list = []
    with open(herbs_list_file, 'r', encoding='utf-8') as f:
        herbs_list = json.load(f)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        for item in data:
            medicines = item['标准处方药材名称']
            # 这里需要对medicines使用、进行分割处理
            medicines = medicines.split('、')
            for medicine in medicines:
                if medicine in herbs_list:
                    print(f"删除的样本: {item}")
                    data.remove(item)
                    break
    print(f"最终样本数量: {len(data)}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return 

# 读取json文件，统计json数据的样本个数
def count_len(path = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid_remove_low.json'):
    count = 0
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        count = len(data)
    print(f"样本个数: {count}")
def sort(input_file = 'data/enhanced_symptom_herb_relationships.json'):

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key, value in data.items():
            sort_item = sorted(value.items(), key=lambda x: x[1], reverse=True)
            data[key] = dict(sort_item)
    # 重新打开文件进行写入
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # #第一步删除病案无效的样本
    # main(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3.json', 
    # output_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json')
    # #第二步统计药材名称出现的次数
    # medicine_counts = count_unique_medicines(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json', 
    # output_file = '/media/data4/yangcm/tcm_data_construct/data/herbs.json')
    # #第三步统计Materials.json中Materials.json中药材名称出现的次数低于322次的 Material
    # low_frequency_medicines = count_low_frequency_medicines(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json', 
    # output_file = '/media/data4/yangcm/tcm_data_construct/data/herbs_list_name_low_322.json')
    # # 第四步删除Materials.json中Materials.json中药材名称出现的次数低于322次的 Material
    # remove_low_frequency_medicines(input_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid.json', 
    #         output_file = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid_remove_low.json',
    #         herbs_list_file = '/media/data4/yangcm/tcm_data_construct/data/herbs_list_name_low_322.json')
    # count_len(path = '/media/data4/yangcm/tcm_data_construct/data/data_cleaned_v3_valid_remove_low.json')
    # count_unique_medicines(input_file = './data/data_cleaned_v4.json', output_file = './data/herbs_v4.json')
    sort()