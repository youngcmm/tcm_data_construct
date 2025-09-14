import numpy as np
import json

def count_overlap(list1, list2):
    return (set(list1) & set(list2))

def evaluate_herbs(pred: str, grt: str, func_list: dict, N: int, eval_type: str, strict: str):
    """
    args:
    pred：string 类型，预测药物。示例："山药，甘草，茯苓，川芎，山萸肉，酸枣仁，附子，泽泻，地黄，牡丹皮，知母，桂枝"。需要以中文逗号进行分隔。
    grt：string 类型，实际药物。示例："豆豉，陈皮，桔梗，知母，远志，甘草，栀子，百合，地黄，合欢皮，茯苓，石菖蒲，竹茹"
    func_list：dict 类型，输入 herb2func.json 读取的内容。
    N：int 类型，允许重叠的药物功效数量，仅接收正整数输入。
    eval_type：string 类型，支持两种模式 iou 与 f1。前者仅返回 iou，后者返回查准率，召回率与 F1-Score
    strict：bool 类型，如果为 true 则不采用功效评估，仅以名称严格匹配药物
    """
    matched = 0
    pred = pred.split("，")
    grt = grt.split("，")
    overlap = count_overlap(pred, grt)
    matched += len(overlap)
    pred_len, grt_len = len(pred), len(grt)
    total_len = len(set(pred + grt))

    if strict:
        if eval_type == 'iou':
            return matched / total_len
        elif eval_type == 'f1':
            precision = matched / pred_len
            recall = matched / grt_len
            f1 = 2 * precision * recall / (precision + recall)
            return precision, recall, f1
        else:
            raise NotImplementedError('evaluate type: iou & f1 is supported.')

    # 首先计算完全匹配的药物，并去掉这些完全匹配的药
    for ov in overlap:
        pred.remove(ov)
        grt.remove(ov)

    # 然后计算部分匹配的药物，优先选用匹配程度最高的药物。
    sub_match = []
    for pr in pred:
        pr_func = func_list[pr].split("，")
        pr_match_num = []
        for gt in grt:
            gt_func = func_list[gt].split("，")
            pr_match_num.append(len(count_overlap(pr_func, gt_func)))
        sub_match.append(pr_match_num)
    sub_match = np.array(sub_match)                                 # 行：pred 的药物  列：gt 的药物和 pred 匹配的功效数量
    
    while (sub_match.max() >= N):
        max_idx = np.where(sub_match == sub_match.max())
        matched += min(len(set(max_idx[0])), len(set(max_idx[1])))  # 只统计功效重叠数符合要求，并且匹配程度最优的药，并且同行同列进行去重
        for i in max_idx[0]:
            for j in max_idx[1]:
                if sub_match[i,j] == -1: continue                   # 防止药品在没有被匹配的情况下被置为 -1，失去后续匹配的资格
                sub_match[i,:] = -1
                sub_match[:,j] = -1                                 # 在统计完成后，将同行同列全部置为 -1，避免重复
    
    if eval_type == 'iou':
        return matched / total_len
    elif eval_type == 'f1':
        precision = matched / pred_len
        recall = matched / grt_len
        f1 = 2 * precision * recall / (precision + recall)
        return precision, recall, f1
    else:
        raise NotImplementedError('evaluate type: iou & f1 is supported.')


# 以下是一个示例：
pred = "山药，甘草，茯苓，川芎，山萸肉，酸枣仁，附子，泽泻，地黄，牡丹皮，知母，桂枝"
grt = "豆豉，陈皮，桔梗，知母，远志，甘草，栀子，百合，地黄，合欢皮，茯苓，石菖蒲，竹茹"
with open('./herbs_func/herb2func.json', 'r', encoding='utf-8') as f:
    func_list = json.load(f)
precision, recall, f1 = evaluate_herbs(pred, grt, func_list, 2, 'f1', True)
print('precision: ', precision, 'recall: ', recall, 'f1: ', f1)