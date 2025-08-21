import pandas as pd
import re
from tqdm import tqdm
import time

# 处方标准化,并统计总的药材数量以及前10种最常用的药材。

def extract_herbs(text, substitution_dict=None):
    """从中药处方文本中提取标准化药材名称"""
    if pd.isna(text) or not text:
        return ''
    
    # 使用正则表达式匹配 {药材名称}{剂量}{单位} 格式
    pattern = r'\{([^}]+)\}\{[\d.]+\}\{[^}]+\}'
    matches = re.findall(pattern, text)
    
    if not matches:
        return ''
    
    # 标准化药材名称
    standardized_herbs = []
    for herb in matches:
        # 去除括号内容，提取主要药材名称
        
        # 处理（）和()两种括号
        clean_herb = re.sub(r'[（(][^）)]*[）)]', '', herb)
        
        # 处理颗粒和珠
        clean_herb = re.sub(r'([^(]+)颗粒', r'\1', clean_herb) 
        clean_herb = re.sub(r'([^(]+)珠', r'\1', clean_herb)
        
        # 使用预编译的字典进行批量替换
        if substitution_dict:
            for pattern, replacement in substitution_dict.items():
                clean_herb = pattern.sub(replacement, clean_herb)
        else:
            # 药物名称标准化，通过herb_uniq.py得到标准化处理映射关系
            clean_herb = re.sub(r'茯神', '茯苓', clean_herb)
            clean_herb = re.sub(r'炙杷叶', '枇杷叶', clean_herb)
            clean_herb = re.sub(r'桔络', '橘络', clean_herb)
            clean_herb = re.sub(r'桔核', '橘核', clean_herb)           
            clean_herb = re.sub(r'枸杞根', '地骨皮', clean_herb)
            clean_herb = re.sub(r'叶下', '叶下珠', clean_herb)
            clean_herb = re.sub(r'三七片', '三七', clean_herb)
            clean_herb = re.sub(r'三七粉', '三七', clean_herb)
            clean_herb = re.sub(r'熟三七粉', '三七', clean_herb)
            clean_herb = re.sub(r'醋三棱', '三棱', clean_herb)
            clean_herb = re.sub(r'粤丝瓜络', '丝瓜络', clean_herb)
            clean_herb = re.sub(r'乌梅炭', '乌梅', clean_herb)
            clean_herb = re.sub(r'酒乌梢蛇', '乌梢蛇', clean_herb)
            clean_herb = re.sub(r'乌豆衣', '乌豆', clean_herb)
            clean_herb = re.sub(r'炒九香虫', '九香虫', clean_herb)
            clean_herb = re.sub(r'醋乳香', '乳香', clean_herb)
            clean_herb = re.sub(r'醋五味子', '五味子', clean_herb)
            clean_herb = re.sub(r'醋五灵脂', '五灵脂', clean_herb)
            clean_herb = re.sub(r'人参叶', '人参', clean_herb)
            clean_herb = re.sub(r'人参片', '人参', clean_herb)
            clean_herb = re.sub(r'人参配方', '人参', clean_herb)
            clean_herb = re.sub(r'制何首乌', '何首乌', clean_herb)
            clean_herb = re.sub(r'炒僵蚕', '僵蚕', clean_herb)
            clean_herb = re.sub(r'明党参', '党参', clean_herb)
            clean_herb = re.sub(r'熟党参', '党参', clean_herb)
            clean_herb = re.sub(r'炒六神曲', '六神曲', clean_herb)
            clean_herb = re.sub(r'焦六神曲', '六神曲', clean_herb)
            clean_herb = re.sub(r'炒关黄柏', '关黄柏', clean_herb)
            clean_herb = re.sub(r'盐关黄柏', '关黄柏', clean_herb)
            clean_herb = re.sub(r'炒冬瓜子', '冬瓜子', clean_herb)
            clean_herb = re.sub(r'炒决明子', '决明子', clean_herb)
            clean_herb = re.sub(r'化橘红胎', '化橘红', clean_herb)
            clean_herb = re.sub(r'厚朴花', '厚朴', clean_herb)
            clean_herb = re.sub(r'姜厚朴', '厚朴', clean_herb)
            clean_herb = re.sub(r'广东合欢花', '合欢花', clean_herb)
            clean_herb = re.sub(r'制吴茱萸', '吴茱萸', clean_herb)
            clean_herb = re.sub(r'生商陆', '商陆', clean_herb)
            clean_herb = re.sub(r'广东土牛膝', '土牛膝', clean_herb)
            clean_herb = re.sub(r'紫花地丁', '地丁', clean_herb)
            clean_herb = re.sub(r'地榆炭', '地榆', clean_herb)
            clean_herb = re.sub(r'地黄炭', '地黄', clean_herb)
            clean_herb = re.sub(r'熟地黄', '地黄', clean_herb)
            clean_herb = re.sub(r'生地黄', '地黄', clean_herb)
            clean_herb = re.sub(r'壁虎粉', '壁虎', clean_herb)
            clean_herb = re.sub(r'大黄炭', '大黄', clean_herb)
            clean_herb = re.sub(r'熟大黄', '大黄', clean_herb)
            clean_herb = re.sub(r'酒大黄', '大黄', clean_herb)
            clean_herb = re.sub(r'人工天竺黄', '天竺黄', clean_herb)
            clean_herb = re.sub(r'酒女贞子', '女贞子', clean_herb)
            clean_herb = re.sub(r'炮姜炭', '姜炭', clean_herb)
            clean_herb = re.sub(r'姜黄连', '姜黄', clean_herb)
            clean_herb = re.sub(r'片姜黄', '姜黄', clean_herb)
            clean_herb = re.sub(r'北寒水石', '寒水石', clean_herb)
            clean_herb = re.sub(r'盐小茴香', '小茴香', clean_herb)
            clean_herb = re.sub(r'小蓟炭', '小蓟', clean_herb)
            clean_herb = re.sub(r'净山楂', '山楂', clean_herb)
            clean_herb = re.sub(r'山楂炭', '山楂', clean_herb)
            clean_herb = re.sub(r'炒山楂', '山楂', clean_herb)
            clean_herb = re.sub(r'焦山楂', '山楂', clean_herb)
            clean_herb = re.sub(r'生山萸肉', '山萸肉', clean_herb)
            clean_herb = re.sub(r'盐山萸肉', '山萸肉', clean_herb)
            clean_herb = re.sub(r'岗梅根', '岗梅', clean_herb)
            clean_herb = re.sub(r'岗稔根', '岗稔', clean_herb)
            clean_herb = re.sub(r'盐巴戟天', '巴戟天', clean_herb)
            clean_herb = re.sub(r'干姜皮', '干姜', clean_herb)
            clean_herb = re.sub(r'醋延胡索', '延胡索', clean_herb)
            clean_herb = re.sub(r'当归炭', '当归', clean_herb)
            clean_herb = re.sub(r'野木瓜', '木瓜', clean_herb)
            clean_herb = re.sub(r'川木通', '木通', clean_herb)
            clean_herb = re.sub(r'盐杜仲', '杜仲', clean_herb)
            clean_herb = re.sub(r'蜜枇杷叶', '枇杷叶', clean_herb)
            clean_herb = re.sub(r'麸炒枳壳', '枳壳', clean_herb)
            clean_herb = re.sub(r'麸炒枳实', '枳实', clean_herb)
            clean_herb = re.sub(r'北柴胡', '柴胡', clean_herb)
            clean_herb = re.sub(r'银柴胡', '柴胡', clean_herb)
            clean_herb = re.sub(r'栀子炭', '栀子', clean_herb)
            clean_herb = re.sub(r'炒栀子', '栀子', clean_herb)
            clean_herb = re.sub(r'焦栀子', '栀子', clean_herb)
            clean_herb = re.sub(r'燀桃仁', '桃仁', clean_herb)
            clean_herb = re.sub(r'老桑枝', '桑枝', clean_herb)
            clean_herb = re.sub(r'槐花炭', '槐花', clean_herb)
            clean_herb = re.sub(r'焦槟榔', '槟榔', clean_herb)
            clean_herb = re.sub(r'盐橘核', '橘核', clean_herb)
            clean_herb = re.sub(r'化橘红', '橘红', clean_herb)
            clean_herb = re.sub(r'紫檀香', '檀香', clean_herb)
            clean_herb = re.sub(r'蜜款冬花', '款冬花', clean_herb)
            clean_herb = re.sub(r'水蛭粉', '水蛭', clean_herb)
            clean_herb = re.sub(r'烫水蛭', '水蛭', clean_herb)
            clean_herb = re.sub(r'盐沙苑子', '沙苑子', clean_herb)
            clean_herb = re.sub(r'广海桐皮', '海桐皮', clean_herb)
            clean_herb = re.sub(r'广东海风藤', '海风藤', clean_herb)
            clean_herb = re.sub(r'成人清热解毒方', '清热解毒方', clean_herb)
            clean_herb = re.sub(r'麸炒薏苡仁', '炒薏苡仁', clean_herb)
            clean_herb = re.sub(r'土牛膝', '牛膝', clean_herb)
            clean_herb = re.sub(r'酒川牛膝', '牛膝', clean_herb)
            clean_herb = re.sub(r'炒牛蒡子', '牛蒡子', clean_herb)
            clean_herb = re.sub(r'煅牡蛎', '牡蛎', clean_herb)
            clean_herb = re.sub(r'烫狗脊', '狗脊', clean_herb)
            clean_herb = re.sub(r'广东王不留行', '王不留行', clean_herb)
            clean_herb = re.sub(r'炒王不留行', '王不留行', clean_herb)
            clean_herb = re.sub(r'琥珀末', '琥珀', clean_herb)
            clean_herb = re.sub(r'瓜蒌仁', '瓜蒌', clean_herb)
            clean_herb = re.sub(r'瓜蒌子', '瓜蒌', clean_herb)
            clean_herb = re.sub(r'瓜蒌皮', '瓜蒌', clean_herb)
            clean_herb = re.sub(r'煅瓦楞子', '瓦楞子', clean_herb)
            clean_herb = re.sub(r'炙甘草', '甘草', clean_herb)
            clean_herb = re.sub(r'醋甘遂', '甘遂', clean_herb)
            clean_herb = re.sub(r'生姜粉', '生姜', clean_herb)
            clean_herb = re.sub(r'白及&#x0D;', '白及', clean_herb)
            clean_herb = re.sub(r'白及粉', '白及', clean_herb)
            clean_herb = re.sub(r'炒白扁豆', '白扁豆', clean_herb)
            clean_herb = re.sub(r'土白术', '白术', clean_herb)
            clean_herb = re.sub(r'麸炒白术', '白术', clean_herb)
            clean_herb = re.sub(r'炒白芍', '白芍', clean_herb)
            clean_herb = re.sub(r'酒白芍', '白芍', clean_herb)
            clean_herb = re.sub(r'白茅根炭', '白茅根', clean_herb)
            clean_herb = re.sub(r'蜜百部', '百部', clean_herb)
            clean_herb = re.sub(r'益智仁', '益智', clean_herb)
            clean_herb = re.sub(r'盐益智仁', '益智', clean_herb)
            clean_herb = re.sub(r'干益母草', '益母草', clean_herb)
            clean_herb = re.sub(r'益母草膏', '益母草', clean_herb)
            clean_herb = re.sub(r'干石斛', '石斛', clean_herb)
            clean_herb = re.sub(r'有瓜石斛', '石斛', clean_herb)
            clean_herb = re.sub(r'金钗石斛', '石斛', clean_herb)
            clean_herb = re.sub(r'煅石膏', '石膏', clean_herb)
            clean_herb = re.sub(r'生石膏', '石膏', clean_herb)
            clean_herb = re.sub(r'姜制砂仁米', '砂仁', clean_herb)
            clean_herb = re.sub(r'煅磁石', '磁石', clean_herb)
            clean_herb = re.sub(r'炒稻芽', '稻芽', clean_herb)
            clean_herb = re.sub(r'姜竹茹', '竹茹', clean_herb)
            clean_herb = re.sub(r'新疆紫草', '紫草', clean_herb)
            clean_herb = re.sub(r'生紫菀', '紫菀', clean_herb)
            clean_herb = re.sub(r'蜜紫菀', '紫菀', clean_herb)
            clean_herb = re.sub(r'新开河红参片', '红参', clean_herb)
            clean_herb = re.sub(r'红参片', '红参', clean_herb)
            clean_herb = re.sub(r'灯盏细辛', '细辛', clean_herb)
            clean_herb = re.sub(r'广东络石藤', '络石藤', clean_herb)
            clean_herb = re.sub(r'续断片', '续断', clean_herb)
            clean_herb = re.sub(r'肉桂粉', '肉桂', clean_herb)
            clean_herb = re.sub(r'麸煨肉豆蔻', '肉豆蔻', clean_herb)
            clean_herb = re.sub(r'煅自然铜', '自然铜', clean_herb)
            clean_herb = re.sub(r'艾叶炭', '艾叶', clean_herb)
            clean_herb = re.sub(r'炒芥子', '芥子', clean_herb)
            clean_herb = re.sub(r'麸炒苍术', '苍术', clean_herb)
            clean_herb = re.sub(r'炒苍耳子', '苍耳子', clean_herb)
            clean_herb = re.sub(r'苏铁贯众炭', '苏铁贯众', clean_herb)
            clean_herb = re.sub(r'燀苦杏仁', '苦杏仁', clean_herb)
            clean_herb = re.sub(r'茜草炭', '茜草', clean_herb)
            clean_herb = re.sub(r'土茯苓', '茯苓', clean_herb)
            clean_herb = re.sub(r'茯苓皮', '茯苓', clean_herb)
            clean_herb = re.sub(r'茵陈【滨蒿】', '茵陈', clean_herb)
            clean_herb = re.sub(r'荆芥炭', '荆芥', clean_herb)
            clean_herb = re.sub(r'荆芥穗', '荆芥', clean_herb)
            clean_herb = re.sub(r'醋莪术', '莪术', clean_herb)
            clean_herb = re.sub(r'炒莱菔子', '莱菔子', clean_herb)
            clean_herb = re.sub(r'莲子心', '莲子', clean_herb)
            clean_herb = re.sub(r'野菊花', '菊花', clean_herb)
            clean_herb = re.sub(r'盐菟丝子', '菟丝子', clean_herb)
            clean_herb = re.sub(r'粉萆薢', '萆薢', clean_herb)
            clean_herb = re.sub(r'绵萆薢', '萆薢', clean_herb)
            clean_herb = re.sub(r'煨葛根', '葛根', clean_herb)
            clean_herb = re.sub(r'炒蒲黄', '蒲黄', clean_herb)
            clean_herb = re.sub(r'生蒲黄', '蒲黄', clean_herb)
            clean_herb = re.sub(r'蒲黄炭', '蒲黄', clean_herb)
            clean_herb = re.sub(r'盐蒺藜', '蒺藜', clean_herb)
            clean_herb = re.sub(r'炒蔓荆子', '蔓荆子', clean_herb)
            clean_herb = re.sub(r'蕤仁肉', '蕤仁', clean_herb)
            clean_herb = re.sub(r'炒薏苡仁', '薏苡仁', clean_herb)
            clean_herb = re.sub(r'藁本片', '藁本', clean_herb)
            clean_herb = re.sub(r'藕节炭', '藕节', clean_herb)
            clean_herb = re.sub(r'广藿香', '藿香', clean_herb)
            clean_herb = re.sub(r'海蛤壳', '蛤壳', clean_herb)
            clean_herb = re.sub(r'炒蜂房', '蜂房', clean_herb)
            clean_herb = re.sub(r'盐补骨脂', '补骨脂', clean_herb)
            clean_herb = re.sub(r'煨诃子', '诃子', clean_herb)
            clean_herb = re.sub(r'谷精草', '谷精', clean_herb)
            clean_herb = re.sub(r'炒谷芽', '谷芽', clean_herb)
            clean_herb = re.sub(r'生谷芽', '谷芽', clean_herb)
            clean_herb = re.sub(r'肉豆蔻', '豆蔻', clean_herb)
            clean_herb = re.sub(r'草豆蔻', '豆蔻', clean_herb)
            clean_herb = re.sub(r'煅赭石', '赭石', clean_herb)
            clean_herb = re.sub(r'盐车前子', '车前子', clean_herb)
            clean_herb = re.sub(r'制远志', '远志', clean_herb)
            clean_herb = re.sub(r'蜜远志', '远志', clean_herb)
            clean_herb = re.sub(r'小通草', '通草', clean_herb)
            clean_herb = re.sub(r'炒酸枣仁', '酸枣仁', clean_herb)
            clean_herb = re.sub(r'醋没药颗粒', '醋没药', clean_herb)
            clean_herb = re.sub(r'金樱子肉', '金樱子', clean_herb)
            clean_herb = re.sub(r'广金钱草', '金钱草', clean_herb)
            clean_herb = re.sub(r'制白附子', '附子', clean_herb)
            clean_herb = re.sub(r'熟附子', '附子', clean_herb)
            clean_herb = re.sub(r'淡附片', '附子', clean_herb)
            clean_herb = re.sub(r'炮附片', '附子', clean_herb)
            clean_herb = re.sub(r'广陈皮', '陈皮', clean_herb)
            clean_herb = re.sub(r'新会陈皮', '陈皮', clean_herb)
            clean_herb = re.sub(r'成人风寒解毒方', '风寒解毒方', clean_herb)
            clean_herb = re.sub(r'成人风热解毒方', '风热解毒方', clean_herb)
            clean_herb = re.sub(r'醋香附', '香附', clean_herb)
            clean_herb = re.sub(r'烫骨碎补', '骨碎补', clean_herb)
            clean_herb = re.sub(r'高丽参粉', '高丽参', clean_herb)
            clean_herb = re.sub(r'干鱼腥草', '鱼腥草', clean_herb)
            clean_herb = re.sub(r'炒鸡内金', '鸡内金', clean_herb)
            clean_herb = re.sub(r'鹿角末', '鹿角', clean_herb)
            clean_herb = re.sub(r'鹿角粉', '鹿角', clean_herb)
            clean_herb = re.sub(r'鹿角胶', '鹿角', clean_herb)
            clean_herb = re.sub(r'鹿角霜', '鹿角', clean_herb)
            clean_herb = re.sub(r'毛麝香', '麝香', clean_herb)
            clean_herb = re.sub(r'炒麦芽', '麦芽', clean_herb)
            clean_herb = re.sub(r'焦麦芽', '麦芽', clean_herb)
            clean_herb = re.sub(r'蜜麻黄', '麻黄', clean_herb)
            clean_herb = re.sub(r'麻黄根', '麻黄', clean_herb)
            clean_herb = re.sub(r'关黄柏', '黄柏', clean_herb)
            clean_herb = re.sub(r'盐黄柏', '黄柏', clean_herb)
            clean_herb = re.sub(r'酒黄精', '黄精', clean_herb)
            clean_herb = re.sub(r'黄芩片', '黄芩', clean_herb)
            clean_herb = re.sub(r'炙黄芪', '黄芪', clean_herb)
            clean_herb = re.sub(r'炒黄连', '黄连', clean_herb)
            clean_herb = re.sub(r'胡黄连', '黄连', clean_herb)
            clean_herb = re.sub(r'萸黄连', '黄连', clean_herb)
            clean_herb = re.sub(r'黄连片', '黄连', clean_herb)
            clean_herb = re.sub(r'鲜龙葵果', '龙葵', clean_herb)
            clean_herb = re.sub(r'龙葵果', '龙葵', clean_herb)
            clean_herb = re.sub(r'煅龙骨', '龙骨', clean_herb)
            clean_herb = re.sub(r'醋龟甲', '龟甲', clean_herb)
            clean_herb = re.sub(r'龟甲胶', '龟甲', clean_herb)
            clean_herb = re.sub(r'土贝母', '贝母', clean_herb)
            clean_herb = re.sub(r'川贝母', '贝母', clean_herb)
            clean_herb = re.sub(r'浙贝母', '贝母', clean_herb)
            clean_herb = re.sub(r'淡豆豉', '豆豉', clean_herb)
            clean_herb = re.sub(r'豆豉姜', '豆豉', clean_herb)
            clean_herb = re.sub(r'半夏曲', '半夏', clean_herb)
            clean_herb = re.sub(r'姜半夏', '半夏', clean_herb)
            clean_herb = re.sub(r'法半夏', '半夏', clean_herb)
            clean_herb = re.sub(r'清半夏', '半夏', clean_herb)
            clean_herb = re.sub(r'生半夏', '半夏', clean_herb)
            clean_herb = re.sub(r'中药特殊调配-煎膏调配', '', clean_herb)
            clean_herb = re.sub(r'煎药机煎药 医生禁用', '', clean_herb)

        #匹配人工煎药用空格替代
        clean_herb = re.sub(r'人工煎药', '', clean_herb)
        
        # 去除多余空格
        clean_herb = clean_herb.strip()
        if clean_herb:
            standardized_herbs.append(clean_herb)
    
    # 用顿号连接
    return '、'.join(standardized_herbs)

def create_substitution_dict():
    """创建预编译的替换字典以提高性能"""
    # 定义替换规则
    substitution_rules = {
        r'茯神':'茯苓',
        r'桔核':'橘核',
        r'叶下':'叶下珠',
        r'枸杞根':'地骨皮',
        r'三七片': '三七',
        r'三七粉': '三七',
        r'熟三七粉': '三七',
        r'醋三棱': '三棱',
        r'粤丝瓜络': '丝瓜络',
        r'乌梅炭': '乌梅',
        r'酒乌梢蛇': '乌梢蛇',
        r'乌豆衣': '乌豆',
        r'炒九香虫': '九香虫',
        r'醋乳香': '乳香',
        r'醋五味子': '五味子',
        r'醋五灵脂': '五灵脂',
        r'人参叶': '人参',
        r'人参片': '人参',
        r'人参配方': '人参',
        r'制何首乌': '何首乌',
        r'炒僵蚕': '僵蚕',
        r'明党参': '党参',
        r'熟党参': '党参',
        r'炒六神曲': '六神曲',
        r'焦六神曲': '六神曲',
        r'炒关黄柏': '关黄柏',
        r'盐关黄柏': '关黄柏',
        r'炒冬瓜子': '冬瓜子',
        r'炒决明子': '决明子',
        r'化橘红胎': '化橘红',
        r'厚朴花': '厚朴',
        r'姜厚朴': '厚朴',
        r'广东合欢花': '合欢花',
        r'制吴茱萸': '吴茱萸',
        r'生商陆': '商陆',
        r'广东土牛膝': '土牛膝',
        r'紫花地丁': '地丁',
        r'地榆炭': '地榆',
        r'地黄炭': '地黄',
        r'熟地黄': '地黄',
        r'生地黄': '地黄',
        r'壁虎粉': '壁虎',
        r'大黄炭': '大黄',
        r'熟大黄': '大黄',
        r'酒大黄': '大黄',
        r'人工天竺黄': '天竺黄',
        r'酒女贞子': '女贞子',
        r'炮姜炭': '姜炭',
        r'姜黄连': '姜黄',
        r'片姜黄': '姜黄',
        r'北寒水石': '寒水石',
        r'盐小茴香': '小茴香',
        r'小蓟炭': '小蓟',
        r'净山楂': '山楂',
        r'山楂炭': '山楂',
        r'炒山楂': '山楂',
        r'焦山楂': '山楂',
        r'生山萸肉': '山萸肉',
        r'盐山萸肉': '山萸肉',
        r'岗梅根': '岗梅',
        r'岗稔根': '岗稔',
        r'盐巴戟天': '巴戟天',
        r'干姜皮': '干姜',
        r'醋延胡索': '延胡索',
        r'当归炭': '当归',
        r'野木瓜': '木瓜',
        r'川木通': '木通',
        r'盐杜仲': '杜仲',
        r'蜜枇杷叶': '枇杷叶',
        r'麸炒枳壳': '枳壳',
        r'麸炒枳实': '枳实',
        r'北柴胡': '柴胡',
        r'银柴胡': '柴胡',
        r'栀子炭': '栀子',
        r'炒栀子': '栀子',
        r'焦栀子': '栀子',
        r'燀桃仁': '桃仁',
        r'老桑枝': '桑枝',
        r'槐花炭': '槐花',
        r'焦槟榔': '槟榔',
        r'盐橘核': '橘核',
        r'化橘红': '橘红',
        r'紫檀香': '檀香',
        r'蜜款冬花': '款冬花',
        r'水蛭粉': '水蛭',
        r'烫水蛭': '水蛭',
        r'盐沙苑子': '沙苑子',
        r'广海桐皮': '海桐皮',
        r'广东海风藤': '海风藤',
        r'成人清热解毒方': '清热解毒方',
        r'麸炒薏苡仁': '炒薏苡仁',
        r'土牛膝': '牛膝',
        r'酒川牛膝': '牛膝',
        r'炒牛蒡子': '牛蒡子',
        r'煅牡蛎': '牡蛎',
        r'烫狗脊': '狗脊',
        r'广东王不留行': '王不留行',
        r'炒王不留行': '王不留行',
        r'琥珀末': '琥珀',
        r'瓜蒌仁': '瓜蒌',
        r'瓜蒌子': '瓜蒌',
        r'瓜蒌皮': '瓜蒌',
        r'煅瓦楞子': '瓦楞子',
        r'炙甘草': '甘草',
        r'醋甘遂': '甘遂',
        r'生姜粉': '生姜',
        r'白及&#x0D;': '白及',
        r'白及粉': '白及',
        r'炒白扁豆': '白扁豆',
        r'土白术': '白术',
        r'麸炒白术': '白术',
        r'炒白芍': '白芍',
        r'酒白芍': '白芍',
        r'白茅根炭': '白茅根',
        r'蜜百部': '百部',
        r'益智仁': '益智',
        r'盐益智仁': '益智',
        r'干益母草': '益母草',
        r'益母草膏': '益母草',
        r'干石斛': '石斛',
        r'有瓜石斛': '石斛',
        r'金钗石斛': '石斛',
        r'煅石膏': '石膏',
        r'生石膏': '石膏',
        r'姜制砂仁米': '砂仁',
        r'煅磁石': '磁石',
        r'炒稻芽': '稻芽',
        r'姜竹茹': '竹茹',
        r'新疆紫草': '紫草',
        r'生紫菀': '紫菀',
        r'蜜紫菀': '紫菀',
        r'新开河红参片': '红参',
        r'红参片': '红参',
        r'灯盏细辛': '细辛',
        r'广东络石藤': '络石藤',
        r'续断片': '续断',
        r'肉桂粉': '肉桂',
        r'麸煨肉豆蔻': '肉豆蔻',
        r'煅自然铜': '自然铜',
        r'艾叶炭': '艾叶',
        r'炒芥子': '芥子',
        r'麸炒苍术': '苍术',
        r'炒苍耳子': '苍耳子',
        r'苏铁贯众炭': '苏铁贯众',
        r'燀苦杏仁': '苦杏仁',
        r'茜草炭': '茜草',
        r'土茯苓': '茯苓',
        r'茯苓皮': '茯苓',
        r'茵陈【滨蒿】': '茵陈',
        r'荆芥炭': '荆芥',
        r'荆芥穗': '荆芥',
        r'醋莪术': '莪术',
        r'炒莱菔子': '莱菔子',
        r'莲子心': '莲子',
        r'野菊花': '菊花',
        r'盐菟丝子': '菟丝子',
        r'粉萆薢': '萆薢',
        r'绵萆薢': '萆薢',
        r'煨葛根': '葛根',
        r'炒蒲黄': '蒲黄',
        r'生蒲黄': '蒲黄',
        r'蒲黄炭': '蒲黄',
        r'盐蒺藜': '蒺藜',
        r'炒蔓荆子': '蔓荆子',
        r'蕤仁肉': '蕤仁',
        r'炒薏苡仁': '薏苡仁',
        r'藁本片': '藁本',
        r'藕节炭': '藕节',
        r'广藿香': '藿香',
        r'海蛤壳': '蛤壳',
        r'炒蜂房': '蜂房',
        r'盐补骨脂': '补骨脂',
        r'煨诃子': '诃子',
        r'谷精草': '谷精',
        r'炒谷芽': '谷芽',
        r'生谷芽': '谷芽',
        r'肉豆蔻': '豆蔻',
        r'草豆蔻': '豆蔻',
        r'煅赭石': '赭石',
        r'盐车前子': '车前子',
        r'制远志': '远志',
        r'蜜远志': '远志',
        r'小通草': '通草',
        r'炒酸枣仁': '酸枣仁',
        r'醋没药颗粒': '醋没药',
        r'金樱子肉': '金樱子',
        r'广金钱草': '金钱草',
        r'制白附子': '附子',
        r'熟附子': '附子',
        r'淡附片': '附子',
        r'炮附片': '附子',
        r'广陈皮': '陈皮',
        r'新会陈皮': '陈皮',
        r'成人风寒解毒方': '风寒解毒方',
        r'成人风热解毒方': '风热解毒方',
        r'醋香附': '香附',
        r'烫骨碎补': '骨碎补',
        r'高丽参粉': '高丽参',
        r'干鱼腥草': '鱼腥草',
        r'炒鸡内金': '鸡内金',
        r'鹿角末': '鹿角',
        r'鹿角粉': '鹿角',
        r'鹿角胶': '鹿角',
        r'鹿角霜': '鹿角',
        r'毛麝香': '麝香',
        r'炒麦芽': '麦芽',
        r'焦麦芽': '麦芽',
        r'蜜麻黄': '麻黄',
        r'麻黄根': '麻黄',
        r'关黄柏': '黄柏',
        r'盐黄柏': '黄柏',
        r'酒黄精': '黄精',
        r'黄芩片': '黄芩',
        r'炙黄芪': '黄芪',
        r'炒黄连': '黄连',
        r'胡黄连': '黄连',
        r'萸黄连': '黄连',
        r'黄连片': '黄连',
        r'鲜龙葵果': '龙葵',
        r'龙葵果': '龙葵',
        r'煅龙骨': '龙骨',
        r'醋龟甲': '龟甲',
        r'龟甲胶': '龟甲',
        r'土贝母': '贝母',
        r'川贝母': '贝母',
        r'浙贝母': '贝母',
        r'淡豆豉': '豆豉',
        r'豆豉姜': '豆豉',
        r'半夏曲': '半夏',
        r'姜半夏': '半夏',
        r'法半夏': '半夏',
        r'清半夏': '半夏',
        r'生半夏': '半夏',
        r'中药特殊调配-煎膏调配': '',
        r'煎药机煎药 医生禁用': '',
    }
    
    # 预编译正则表达式以提高性能
    compiled_dict = {}
    for pattern, replacement in substitution_rules.items():
        compiled_dict[re.compile(pattern)] = replacement
    
    return compiled_dict

def process_prescription_data(input_file, output_file):
    """处理中药处方数据"""
    # 读取CSV文件
    df = pd.read_csv(input_file)
    
    print(f"原始数据量: {len(df)}")
    print(f"数据列名: {df.columns.tolist()}")
    
    # 检查中药处方列是否存在
    if '中药处方' not in df.columns:
        print("错误：未找到'中药处方'列")
        return
    
    # 创建预编译的替换字典
    print("正在预编译替换规则...")
    substitution_dict = create_substitution_dict()
    print(f"已预编译 {len(substitution_dict)} 条替换规则")
    
    # 提取标准化药材名称（带进度条）
    print("正在处理处方数据...")
    start_time = time.time()
    
    # 使用tqdm显示进度条
    df['标准处方药材名称'] = [
        extract_herbs(text, substitution_dict) 
        for text in tqdm(df['中药处方'], total=len(df), desc="处理进度")
    ]
    
    end_time = time.time()
    print(f"处理完成，耗时: {end_time - start_time:.2f} 秒")
    
    # 统计处理结果
    total_prescriptions = len(df)
    valid_prescriptions = df['标准处方药材名称'].str.len() > 0
    valid_count = valid_prescriptions.sum()
    
    print(f"\n处理结果:")
    print(f"总处方数: {total_prescriptions}")
    print(f"成功提取的处方数: {valid_count}")
    print(f"提取成功率: {valid_count/total_prescriptions*100:.2f}%")
    
    # 显示一些示例
    print(f"\n=== 处理示例 ===")
    for i in range(min(5, len(df))):
        if pd.notna(df.iloc[i]['中药处方']) and df.iloc[i]['标准处方药材名称']:
            print(f"\n示例 {i+1}:")
            print(f"原始: {df.iloc[i]['中药处方'][:100]}...")
            print(f"提取: {df.iloc[i]['标准处方药材名称']}")
    
    # 统计最常用的药材
    print(f"\n=== 药材使用频率统计 ===")
    all_herbs = []
    for herbs_str in df['标准处方药材名称'].dropna():
        if herbs_str:
            herbs_list = herbs_str.split('、')
            all_herbs.extend(herbs_list)
    
    if all_herbs:
        herb_counts = pd.Series(all_herbs).value_counts()
        print(f"总药材种类数: {len(herb_counts)}")
        print(f"前10种最常用药材:")
        for i, (herb, count) in enumerate(herb_counts.head(10).items()):
            print(f"{i+1}. {herb}: {count}次")

    ##############################
    #统计有多少处方是相同的，有多少类处方。
    ###############################
    
    # 统计处方类别
    print(f"\n=== 处方类别统计 ===")
    prescription_counts = df['标准处方药材名称'].dropna().value_counts()
    unique_prescriptions = len(prescription_counts)
    total_valid_prescriptions = prescription_counts.sum()
    
    print(f"处方类别总数: {unique_prescriptions}")
    print(f"有效处方总数: {total_valid_prescriptions}")
    
    # 显示最常见的处方
    print(f"\n前10种最常见的处方:")
    for i, (prescription, count) in enumerate(prescription_counts.head(10).items()):
        print(f"{i+1}. 出现{count}次: {prescription[:50]}{'...' if len(prescription) > 50 else ''}")
    
    # 统计处方重复情况
    single_use = (prescription_counts == 1).sum()
    multiple_use = (prescription_counts > 1).sum()
    
    print(f"\n处方重复情况:")
    print(f"仅使用1次的处方: {single_use}个 ({single_use/unique_prescriptions*100:.1f}%)")
    print(f"使用多次的处方: {multiple_use}个 ({multiple_use/unique_prescriptions*100:.1f}%)")
    
    # 处方长度统计
    prescription_lengths = df['标准处方药材名称'].dropna().apply(lambda x: len(x.split('、')) if x else 0)
    
    #重新统计中药剂数
    df['中药剂数'] = prescription_lengths
    print(f"\n处方药材数量统计:")
    print(f"平均每个处方包含药材数: {prescription_lengths.mean():.1f}种")
    print(f"最少药材数: {prescription_lengths.min()}种")
    print(f"最多药材数: {prescription_lengths.max()}种")
    
    # 保存处理后的数据
    df.to_csv(output_file, index=False)
    print(f"\n处理后的数据已保存至: {output_file}")
    
    return df

if __name__ == "__main__":
    # 使用示例
    input_file = '/Volumes/KINGSTON/code/tcm_data_construct/data/20250718-2-失眠病历数据-仅含有睡眠障碍行的数据.csv'
    output_file = '/Volumes/KINGSTON/code/tcm_data_construct/data/20250718-2-失眠病历数据-仅含有睡眠障碍行的数据.csv'
    
    # 处理完整数据
    df = process_prescription_data(input_file, output_file)