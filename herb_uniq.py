import re
# 在提取处方中所有使用的草药名称到herbs.txt之后，将寻找所有炮制后的草药名称，创建脚本clean_herb = re.sub(r'山楂炭', '山楂', clean_herb)，并删除herbs.txt文件中的炮制后的草药名称

def generate_herb_substitutions(base_herb_name, herbs_file='herbs.txt'):
    """
    Generate regex substitution patterns for processed herb forms
    
    Args:
        base_herb_name (str): The base herb name (e.g., '山楂')
        herbs_file (str): Path to the file containing processed herb forms
    """
    
    # Read processed herb forms from file
    try:
        with open(herbs_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File {herbs_file} not found.")
        return
    
    # Split content into lines and clean up
    processed_forms = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Find processed forms that contain the base herb name
    matching_forms = [form for form in processed_forms if base_herb_name in form and form != base_herb_name]
    
    if matching_forms: #如果没有匹配到直接返回。
        print(f"Found {len(matching_forms)} processed forms containing {base_herb_name}:")
        for form in matching_forms:
            print(form)
    else:
        return 
    # Generate substitution patterns
    substitutions = []
    for form in matching_forms:
        substitution = f"        clean_herb = re.sub(r'{form}', '{base_herb_name}', clean_herb)"
        substitutions.append(substitution)
    
    # Write to output file
    output_filename = f"results_substitutions.txt"
    with open(output_filename, 'a', encoding='utf-8') as f:
        for sub in substitutions:
            f.write(sub + '\n')
    
    # Create updated herbs file without the processed forms
    remaining_herbs = [form for form in processed_forms if form not in matching_forms]
    with open(f"{herbs_file}", 'w', encoding='utf-8') as f:
        for herb in remaining_herbs:
            f.write(herb + '\n')
    
    print(f"Generated {len(substitutions)} substitution patterns for {base_herb_name}")
    print(f"Patterns saved to {output_filename}")
    print(f"Updated herbs list saved to {herbs_file}")
    print("\nGenerated patterns:")
    for sub in substitutions:
        print(sub)

if __name__ == "__main__":
    #读取herbs.txt文件的每一行，并生成处理后的草药名称
    # for line in open('/Users/ycm/Library/Mobile Documents/com~apple~CloudDocs/data/herbs_copy.txt', encoding='utf-8'):
    #     herb_name = line.strip()
    #     generate_herb_substitutions(herb_name)

        generate_herb_substitutions('半夏')