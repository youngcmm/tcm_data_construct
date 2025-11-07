#读取睡眠病历问答对.json，随机采样2万个样本作为测试集，剩下的作为训练数据集。
import json
import random

with open('data/concatenated_tcm_data_clean_v1.json', 'r') as f:
    data = json.load(f)

random.shuffle(data)

# 分割数据
test_data = data[:10000]
train_data = data[10000:]

# 保存测试集
with open('data/processed_data_test.json', 'w') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=4)

# 保存训练集
with open('data/processed_data_train.json', 'w') as f:
    json.dump(train_data, f, ensure_ascii=False, indent=4)

print(f"测试集样本数: {len(test_data)}")
print(f"训练集样本数: {len(train_data)}")