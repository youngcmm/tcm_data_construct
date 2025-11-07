import json
import re
from collections import defaultdict, Counter
from itertools import combinations

class EnhancedHerbAnalyzer:
    def __init__(self, data_file="data/concatenated_tcm_data_clean_v1.json"):
        """
        Initialize the analyzer with the data file
        """
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Initialize patterns for symptom extraction
        self._initialize_symptom_patterns()
        
    def _initialize_symptom_patterns(self):
        """
        Initialize patterns for symptom extraction
        """
        self.symptom_patterns = {
            '失眠': r'(失眠|眠差|入睡困难|难以入睡|睡不着|睡眠不佳|睡眠障碍|睡眠欠佳|睡眠差)',
            '多梦': r'(多梦|梦多|梦纷乱|噩梦)',
            '早醒': r'(早醒|醒后难续|醒后难以入睡|凌晨醒)',
            '易醒': r'(易醒|眠浅|睡眠浅)',
            '口干': r'(口干|口干渴|口干苦)',
            '口苦': r'(口苦|口苦口干)',
            '心慌': r'(心慌|心悸|心烦|心神不宁)',
            '头痛': r'(头痛|头晕|头昏|头胀|头重|头麻|巅顶痛)',
            '出汗': r'(汗出|出汗|汗多|汗少|汗出多|盗汗|汗多出|汗出多|自汗)',
            '尿频': r'(尿频|小便频|夜尿|小便多|尿多)',
            '便秘': r'(便秘|大便干|大便硬|大便结|便干|便结)',
            '腹泻': r'(腹泻|便溏|大便稀|大便软|大便烂|便稀|便烂)',
            '食欲': r'(纳可|纳差|食欲|胃纳|纳一般|纳佳|胃纳欠佳)',
            '记忆力下降': r'(记忆力下降|健忘|记忆差|记忆力减退)',
            '情绪': r'(心烦|情志|抑郁|焦虑|心情|烦躁|易怒|情绪低落|情绪不稳|易哭|情绪急躁|情志不畅)',
            '腰酸': r'(腰酸|腰痛|腰酸痛)',
            '性欲': r'(性欲|性功能)',
            '疲倦': r'(疲倦|乏力|精神差|神可|精神不振|精神欠佳|困倦|疲乏|神疲)',
            '怕冷': r'(怕冷|畏寒|恶寒|形寒|肢冷|手足冷)',
            '怕热': r'(怕热|手足热|手心热|脚心热|五心烦热)',
            '潮热': r'潮热',
            '咳嗽': r'(咳嗽|咳痰|咳黄痰)',
            '胸闷': r'(胸闷|胸痛|胸前区不适)',
            '月经': r'(月经|经期|经前|痛经|经量|LMP|PMP|闭经|经期紊乱)',
            '脱发': r'(脱发|掉发|头发脱)',
            '口疮': r'(口疮|口腔溃疡|口疡)',
            '咽痛': r'(咽痛|咽喉痛|咽部不适)',
            '鼻塞': r'(鼻塞|流涕|鼻炎)',
            '耳鸣': r'耳鸣',
            '眼干': r'(眼干|眼涩|目干)',
            '腹胀': r'(腹胀|脘胀|胃脘不适|腹部胀)',
            '嗳气': r'(嗳气|泛酸|反酸)',
            '呕吐': r'(呕吐|恶心|干呕)',
            '打鼾': r'(打鼾|鼾声)',
            '烦躁': r'(烦躁|易怒|心烦|急躁)',
            '健忘': r'(健忘|记忆力下降)',
            '口渴': r'(口渴|欲饮)',
            '夜尿': r'夜尿',
            '多汗': r'多汗|汗多|汗出多',
            '少汗': r'少汗|汗少|汗出少',
            '腰痛': r'腰痛',
            '腰酸': r'腰酸',
            '腰酸痛': r'腰酸痛',
            '胃脘不适': r'(胃脘不适|胃脘痛|胃脘胀)',
            '胃脘痛': r'胃脘痛',
            '胃脘胀': r'胃脘胀',
            '腹痛': r'腹痛',
            '腹胀': r'腹胀',
            '腹泻': r'腹泻',
            '便溏': r'便溏',
            '便干': r'便干',
            '便结': r'便结',
            '便稀': r'便稀',
            '便烂': r'便烂',
            '大便不畅': r'大便不畅',
            '大便粘腻': r'大便粘腻',
            '大便不通': r'大便不通',
            '矢气': r'矢气多|矢气频繁',
            '小便调': r'小便调',
            '小便黄': r'(小便黄|小便短赤|尿黄)',
            '小便频': r'小便频',
            '小便少': r'小便少',
            '小便多': r'小便多',
            '小便不利': r'小便不利',
            '水肿': r'(水肿|浮肿)',
            '肢体麻木': r'(肢体麻木|手麻|脚麻|麻木)',
            '皮肤瘙痒': r'(皮肤瘙痒|瘙痒|皮肤过敏)',
            '皮肤过敏': r'皮肤过敏',
            '皮肤易过敏': r'皮肤易过敏',
            '过敏': r'过敏',
            '过敏性': r'过敏性',
            '过敏反应': r'过敏反应',
            '过敏性疾病': r'过敏性疾病',
            '皮疹': r'皮疹',
            '湿疹': r'湿疹',
            '荨麻疹': r'荨麻疹',
            '痤疮': r'(痤疮|痘痘|青春痘|面疮)',
            '面部痤疮': r'面部痤疮',
            '面部油腻': r'面部油腻',
            '面部色斑': r'面部色斑',
            '面色萎黄': r'面色萎黄',
            '面色无华': r'面色无华',
            '面色': r'面色',
            '神疲': r'神疲',
            '神清': r'神清',
            '精神': r'精神',
            '精神可': r'精神可',
            '精神差': r'精神差',
            '精神不振': r'精神不振',
            '精神欠佳': r'精神欠佳',
            '神志': r'神志',
            '神志清': r'神志清',
            '神志清楚': r'神志清楚',
            '神志不清': r'神志不清',
            '神志模糊': r'神志模糊',
            '神志昏蒙': r'神志昏蒙',
            '神志昏迷': r'神志昏迷',
            '神志障碍': r'神志障碍',
            '神志异常': r'神志异常'
        }
        
        # Extract tongue and pulse information
        self.tongue_patterns = {
            '舌暗红': r'舌暗红',
            '舌淡红': r'舌淡红',
            '舌红': r'舌红(?!苔)',
            '舌淡': r'舌淡(?!苔)',
            '舌淡胖': r'舌淡胖',
            '舌胖大': r'舌胖大',
            '舌暗': r'舌暗',
            '舌嫩': r'舌嫩',
            '舌齿痕': r'(舌.*齿痕|齿印)',
            '舌裂纹': r'(舌.*裂纹|舌.*裂痕)',
            '舌有瘀点': r'舌.*瘀点',
            '苔黄腻': r'苔黄.*腻',
            '苔白腻': r'苔白.*腻',
            '苔薄白': r'苔薄白',
            '苔黄干': r'苔黄.*干',
            '苔薄黄': r'苔薄黄',
            '苔白厚腻': r'苔白.*厚腻',
            '苔微黄': r'苔微黄',
            '苔黄': r'苔黄',
            '苔白': r'苔白(?!腻)',
            '苔薄': r'苔薄',
            '苔厚': r'苔厚',
            '脉弦': r'脉弦',
            '脉细': r'脉细',
            '脉沉': r'脉沉',
            '脉滑': r'脉滑',
            '脉弦细': r'脉弦细',
            '脉弦滑': r'脉弦滑',
            '脉沉细': r'脉沉细',
            '脉沉滑': r'脉沉滑',
            '脉浮': r'脉浮',
            '脉数': r'脉数',
            '脉弱': r'脉弱',
            '脉濡': r'脉濡',
            '脉结代': r'脉结代',
            '脉促': r'脉促',
            '脉迟': r'脉迟',
            '脉紧': r'脉紧',
            '脉洪': r'脉洪',
            '脉微': r'脉微',
            '脉芤': r'脉芤',
            '脉革': r'脉革',
            '脉牢': r'脉牢',
            '脉虚': r'脉虚',
            '脉实': r'脉实',
            '脉长': r'脉长',
            '脉短': r'脉短',
            '脉疾': r'脉疾',
            '脉缓': r'脉缓'
        }

    def extract_symptoms(self, input_text):
        """
        Extract symptoms from the input text
        """
        symptoms = []
        
        # Check for common symptoms
        for symptom, pattern in self.symptom_patterns.items():
            if re.search(pattern, input_text):
                symptoms.append(symptom)
        
        # Check for tongue and pulse symptoms
        for tongue, pattern in self.tongue_patterns.items():
            if re.search(pattern, input_text):
                symptoms.append(tongue)
        
        return symptoms

    def extract_herbs(self, output_text):
        """
        Extract herbs from the output text and sort them
        """
        # Remove the "中药处方：" prefix
        herbs_text = output_text.replace("中药处方：", "").replace("。", "")
        # Split by顿号 (、) and comma (,) to get individual herbs
        herbs = re.split(r'[、,，]', herbs_text.strip())
        # Remove empty strings and whitespace
        herbs = [herb.strip() for herb in herbs if herb.strip()]
        # Sort herbs alphabetically for consistency
        herbs.sort()
        return herbs

    def analyze_herb_cooccurrence(self, min_cooccurrence=10):
        """
        Analyze which herbs commonly appear together
        """
        # Count individual herb frequencies
        herb_counter = Counter()
        
        # Count herb pair co-occurrences
        herb_pair_counter = Counter()
        
        # Count herb triple co-occurrences
        herb_triple_counter = Counter()
        
        # Process each entry
        for entry in self.data:
            output_text = entry.get("output", "")
            herbs = self.extract_herbs(output_text)
            
            # Update individual herb counts
            herb_counter.update(herbs)
            
            # Update herb pair counts (combinations of 2)
            for pair in combinations(herbs, 2):
                herb_pair_counter[pair] += 1
                
            # Update herb triple counts (combinations of 3)
            if len(herbs) >= 3:
                for triple in combinations(herbs, 3):
                    herb_triple_counter[triple] += 1
                
        # Filter pairs by minimum co-occurrence
        filtered_pairs = {pair: count for pair, count in herb_pair_counter.items() 
                         if count >= min_cooccurrence}
                         
        # Filter triples by minimum co-occurrence
        filtered_triples = {triple: count for triple, count in herb_triple_counter.items() 
                           if count >= min_cooccurrence}
        
        return herb_counter, filtered_pairs, filtered_triples

    def analyze_symptom_herb_relationships(self):
        """
        Analyze which symptoms correspond to which herbs
        """
        # Dictionary to store symptom -> herb relationships
        symptom_herb_map = defaultdict(Counter)
        
        # Process each entry
        for entry in self.data:
            input_text = entry.get("input", "")
            output_text = entry.get("output", "")
            
            symptoms = self.extract_symptoms(input_text)
            herbs = self.extract_herbs(output_text)
            
            # Map each symptom to each herb
            for symptom in symptoms:
                for herb in herbs:
                    symptom_herb_map[symptom][herb] += 1
                    
        return symptom_herb_map

    def get_top_cooccurring_herbs(self, herb, herb_pair_counter, top_n=10):
        """
        Get herbs that most commonly co-occur with a given herb
        """
        cooccurring_herbs = Counter()
        
        # Look through all pairs to find ones containing the given herb
        for (herb1, herb2), count in herb_pair_counter.items():
            if herb1 == herb:
                cooccurring_herbs[herb2] = count
            elif herb2 == herb:
                cooccurring_herbs[herb1] = count
                
        return cooccurring_herbs.most_common(top_n)

    def calculate_herb_association_strength(self, herb1, herb2, herb_counter, herb_pair_counter):
        """
        Calculate the association strength between two herbs using PMI (Pointwise Mutual Information)
        """
        # Total number of prescriptions
        total_prescriptions = len(self.data)
        
        # Count of herb1 and herb2
        count1 = herb_counter.get(herb1, 0)
        count2 = herb_counter.get(herb2, 0)
        
        # Count of co-occurrence
        pair_count = 0
        for (h1, h2), count in herb_pair_counter.items():
            if (h1 == herb1 and h2 == herb2) or (h1 == herb2 and h2 == herb1):
                pair_count = count
                break
                
        if count1 == 0 or count2 == 0 or pair_count == 0:
            return 0
            
        # Calculate PMI
        p1 = count1 / total_prescriptions
        p2 = count2 / total_prescriptions
        p12 = pair_count / total_prescriptions
        
        pmi = p12 / (p1 * p2)
        return pmi

    def generate_enhanced_cooccurrence_report(self, min_cooccurrence=10):
        """
        Generate an enhanced report on herb co-occurrence patterns
        """
        print("=== Enhanced Herb Co-occurrence Analysis Report ===")
        
        # Analyze co-occurrence
        herb_counter, herb_pair_counter, herb_triple_counter = self.analyze_herb_cooccurrence(min_cooccurrence)
        
        print(f"\nTotal unique herbs: {len(herb_counter)}")
        print(f"Total herb pairs with co-occurrence >= {min_cooccurrence}: {len(herb_pair_counter)}")
        print(f"Total herb triples with co-occurrence >= {min_cooccurrence}: {len(herb_triple_counter)}")
        
        # Show most common individual herbs
        print("\n=== Most Common Individual Herbs ===")
        for herb, count in herb_counter.most_common(20):
            print(f"{herb}: {count} times ({count/len(self.data)*100:.2f}%)")
            
        # Show most common herb pairs
        print(f"\n=== Most Common Herb Pairs (co-occurrence >= {min_cooccurrence}) ===")
        # Convert dict to Counter for most_common method
        herb_pair_counter_obj = Counter(herb_pair_counter)
        for (herb1, herb2), count in herb_pair_counter_obj.most_common(20):
            print(f"{herb1} + {herb2}: {count} times")
            
        # Show most common herb triples
        print(f"\n=== Most Common Herb Triples (co-occurrence >= {min_cooccurrence}) ===")
        # Convert dict to Counter for most_common method
        herb_triple_counter_obj = Counter(herb_triple_counter)
        for (herb1, herb2, herb3), count in herb_triple_counter_obj.most_common(20):
            print(f"{herb1} + {herb2} + {herb3}: {count} times")
            
        # Show herbs that commonly co-occur with specific herbs
        common_herbs = ['甘草', '茯苓', '酸枣仁', '柴胡', '白术', '牡蛎']
        print(f"\n=== Herbs Commonly Co-occurring with Specific Herbs ===")
        for herb in common_herbs:
            if herb in herb_counter:
                cooccurring = self.get_top_cooccurring_herbs(herb, herb_pair_counter, 10)
                print(f"\n{herb} commonly appears with:")
                for co_herb, count in cooccurring:
                    pmi = self.calculate_herb_association_strength(herb, co_herb, herb_counter, herb_pair_counter)
                    print(f"  {co_herb}: {count} times (PMI: {pmi:.2f})")
                    
        return herb_counter, herb_pair_counter, herb_triple_counter

    def generate_symptom_herb_report(self):
        """
        Generate a comprehensive report on symptom-herb relationships
        """
        print("\n\n=== Symptom-Herb Relationship Analysis Report ===")
        
        # Analyze symptom-herb relationships
        symptom_herb_map = self.analyze_symptom_herb_relationships()
        
        print(f"Total unique symptoms: {len(symptom_herb_map)}")
        
        # Show most common herbs for common symptoms
        common_symptoms = ['失眠', '口干', '心慌', '头痛', '疲倦', '情绪', '出汗', '便秘', '腹泻']
        print("\n=== Most Common Herbs for Common Symptoms ===")
        for symptom in common_symptoms:
            if symptom in symptom_herb_map:
                top_herbs = symptom_herb_map[symptom].most_common(10)
                print(f"\n{symptom}:")
                for herb, count in top_herbs:
                    print(f"  {herb}: {count} times")
                    
        # Show symptoms most treated by common herbs
        common_herbs = ['甘草', '茯苓', '酸枣仁', '柴胡', '白术']
        print("\n\n=== Symptoms Most Treated by Common Herbs ===")
        for herb in common_herbs:
            # Collect all symptoms treated by this herb
            herb_symptoms = Counter()
            for symptom, herbs in symptom_herb_map.items():
                if herb in herbs:
                    herb_symptoms[symptom] = herbs[herb]
            
            print(f"\n{herb} most commonly treats:")
            for symptom, count in herb_symptoms.most_common(10):
                print(f"  {symptom}: {count} times")
                
        return symptom_herb_map

    def save_analysis_results(self, herb_counter, herb_pair_counter, herb_triple_counter, symptom_herb_map):
        """
        Save analysis results to JSON files
        """
        # Save herb co-occurrence data
        cooccurrence_data = {
            "individual_herbs": dict(herb_counter),
            "herb_pairs": {f"{herb1}+{herb2}": count for (herb1, herb2), count in herb_pair_counter.items()},
            "herb_triples": {f"{herb1}+{herb2}+{herb3}": count for (herb1, herb2, herb3), count in herb_triple_counter.items()}
        }
        
        with open("enhanced_herb_cooccurrence.json", 'w', encoding='utf-8') as f:
            json.dump(cooccurrence_data, f, ensure_ascii=False, indent=2)
            
        # Save symptom-herb relationship data
        symptom_herb_data = {
            symptom: dict(herbs) for symptom, herbs in symptom_herb_map.items()
        }
        
        with open("data/enhanced_symptom_herb_relationships.json", 'w', encoding='utf-8') as f:
            json.dump(symptom_herb_data, f, ensure_ascii=False, indent=2)
            
        print("\nAnalysis results saved to enhanced_herb_cooccurrence.json and enhanced_symptom_herb_relationships.json")

    def find_common_herb_combinations_for_symptoms(self, target_symptoms, top_n=5):
        """
        Find common herb combinations for specific symptoms
        """
        # Dictionary to store herb combinations for symptoms
        symptom_herb_combinations = defaultdict(Counter)
        
        # Process each entry
        for entry in self.data:
            input_text = entry.get("input", "")
            output_text = entry.get("output", "")
            
            symptoms = self.extract_symptoms(input_text)
            herbs = self.extract_herbs(output_text)
            
            # Check if all target symptoms are present
            if all(symptom in symptoms for symptom in target_symptoms):
                # Create herb combination key
                herb_combo = "+".join(herbs)
                symptom_combo = "+".join(sorted(target_symptoms))
                symptom_herb_combinations[symptom_combo][herb_combo] += 1
                
        # Get top combinations
        result = {}
        for symptom_combo, herb_combos in symptom_herb_combinations.items():
            result[symptom_combo] = herb_combos.most_common(top_n)
            
        return result

def main():
    # Initialize the analyzer
    analyzer = EnhancedHerbAnalyzer()
    
    # Generate enhanced co-occurrence report
    herb_counter, herb_pair_counter, herb_triple_counter = analyzer.generate_enhanced_cooccurrence_report(5)
    
    # Generate symptom-herb relationship report
    symptom_herb_map = analyzer.generate_symptom_herb_report()
    
    # Save results
    analyzer.save_analysis_results(herb_counter, herb_pair_counter, herb_triple_counter, symptom_herb_map)
    
    # # Example: Find common herb combinations for specific symptoms
    # print("\n\n=== Common Herb Combinations for Specific Symptom Sets ===")
    
    # # Find combinations for insomnia + dry mouth
    # insomnia_dry_mouth_combos = analyzer.find_common_herb_combinations_for_symptoms(['失眠', '口干'], 5)
    # print(f"\nCommon herb combinations for 失眠 + 口干:")
    # for combo, count in insomnia_dry_mouth_combos.get('口干+失眠', []):
    #     print(f"  {combo}: {count} times")
        
    # # Find combinations for insomnia + emotional issues
    # insomnia_emotion_combos = analyzer.find_common_herb_combinations_for_symptoms(['失眠', '情绪'], 5)
    # print(f"\nCommon herb combinations for 失眠 + 情绪:")
    # for combo, count in insomnia_emotion_combos.get('失眠+情绪', []):
    #     print(f"  {combo}: {count} times")
    
    # # Example case analysis
    # print("\n\n=== Example Case Analysis ===")
    # example_output = "中药处方：柴胡、厚朴、乌药、牛膝、白芍、肉桂、浮小麦、半夏、首乌藤、杠板归、牡蛎、合欢皮、桂枝、牡丹皮、龙骨。"
    # herbs = analyzer.extract_herbs(example_output)
    # print(f"Sorted herbs: {', '.join(herbs)}")
    
    # # Show co-occurring herbs for some herbs in the prescription
    # for herb in ['柴胡', '白芍', '半夏', '牡蛎']:
    #     if herb in herbs:
    #         cooccurring = analyzer.get_top_cooccurring_herbs(herb, herb_pair_counter, 5)
    #         print(f"\n{herb} commonly co-occurs with:")
    #         for co_herb, count in cooccurring:
    #             pmi = analyzer.calculate_herb_association_strength(herb, co_herb, herb_counter, herb_pair_counter)
    #             print(f"  {co_herb}: {count} times (PMI: {pmi:.2f})")

if __name__ == "__main__":
    main()