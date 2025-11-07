# 假设您已将JSON数据加载到 all_patient_data = {"6009510110": [visit1, visit2], ...}

def parse_herbs(prescription_str: str) -> set:
    """
    将'酸枣仁、陈皮、茯苓'这样的字符串解析为集合
    """
    if not prescription_str:
        return set()
    return set(prescription_str.split('、'))

def format_herbs_to_string(herb_set: set) -> str:
    """
    将 {"酸枣仁", "陈皮"} 这样的集合转换回标准字符串
    """
    return '、'.join(sorted(list(herb_set)))

def format_visit_summary(visit_data: dict) -> str:
    """
    生成单次就诊的标准化文本摘要
    """
    return f"""
    [第{visit_data['第几次问诊']}次就诊]
    就诊时间: {visit_data['就诊时间']}
    主诉/病史: {visit_data['现病史']}
    舌脉: {visit_data['舌苔脉象']}
    处方: {visit_data['标准处方药材名称']}
    """.strip()