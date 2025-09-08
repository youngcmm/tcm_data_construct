# TCM Data Construction Toolkit

中医药数据清洗、标准化和构建训练数据集工具包

## 功能特性

- 药材名称标准化：统一炮制后的药材名称为标准名称
- 问诊数据清洗：清理无效数据、缺失字段、重复内容等
- 构建结构化问答对：从CSV数据中提取并生成JSON格式的问答训练数据
- 数据过滤：根据长度、内容完整性等条件过滤无效数据

## 脚本说明

### 数据处理脚本

- [herb_uniq.py](file:///media/data4/yangcm/tcm_data_construct/herb_uniq.py)：提取并标准化药材名称
- [extract_herbs.py](file:///media/data4/yangcm/tcm_data_construct/extract_herbs.py)：从中药处方中提取标准化药材
- [generate_qa_pairs.py](file:///media/data4/yangcm/tcm_data_construct/generate_qa_pairs.py)：生成结构化问答对
- [clean_sleep_qa_json_data.py](file:///media/data4/yangcm/tcm_data_construct/clean_sleep_qa_json_data.py)：清洗睡眠相关问答数据
- [filter_nan.py](file:///media/data4/yangcm/tcm_data_construct/filter_nan.py)：过滤空值数据
- [cat_json_data.py](file:///media/data4/yangcm/tcm_data_construct/cat_json_data.py)：合并JSON数据
- [cat_data_here.py](file:///media/data4/yangcm/tcm_data_construct/cat_data_here.py)：将指定目录下所有JSON文件合并
- [count_json_herbs_class.py](file:///media/data4/yangcm/tcm_data_construct/count_json_herbs_class.py)：统计药材类别
- [random_sample.py](file:///media/data4/yangcm/tcm_data_construct/random_sample.py)：随机抽样数据

### 新增功能脚本

- [extract_tcm_features_transformers.py](file:///media/data4/yangcm/tcm_data_construct/extract_tcm_features_transformers.py)：使用Hugging Face Transformers直接加载本地模型，从TCM病案中提取关键症状、舌象、脉象和相关药材

## 使用方法

### 基本数据处理流程

1. 使用 [herb_uniq.py](file:///media/data4/yangcm/tcm_data_construct/herb_uniq.py) 和 [extract_herbs.py](file:///media/data4/yangcm/tcm_data_construct/extract_herbs.py) 标准化药材名称
2. 使用 [generate_qa_pairs.py](file:///media/data4/yangcm/tcm_data_construct/generate_qa_pairs.py) 生成问答对
3. 使用 [clean_sleep_qa_json_data.py](file:///media/data4/yangcm/tcm_data_construct/clean_sleep_qa_json_data.py) 和 [filter_nan.py](file:///media/data4/yangcm/tcm_data_construct/filter_nan.py) 清洗数据
4. 使用 [cat_json_data.py](file:///media/data4/yangcm/tcm_data_construct/cat_json_data.py) 或 [cat_data_here.py](file:///media/data4/yangcm/tcm_data_construct/cat_data_here.py) 合并数据

### 使用LLM提取TCM特征

使用 [extract_tcm_features_transformers.py](file:///media/data4/yangcm/tcm_data_construct/extract_tcm_features_transformers.py) 脚本可以直接加载本地模型并从TCM病案中提取特征：

```bash
python extract_tcm_features_transformers.py
```

该脚本会：
1. 从 `/media/data3/huangjunj/TCM_dataset/cleaned/output_0.json` 加载原始数据
2. 使用Hugging Face Transformers加载位于 `/media/data2/yangcm/models/DeepSeek-R1-Distill-Qwen-32B` 的本地模型
3. 对每个病案提取关键症状、舌象、脉象和相关药材信息
4. 将提取的特征合并到原始数据中
5. 将结果保存到 `data/tcm_extracted_features.json`

## 依赖

请参阅 [requirements.txt](file:///media/data4/yangcm/tcm_data_construct/requirements.txt) 文件了解完整的依赖列表。