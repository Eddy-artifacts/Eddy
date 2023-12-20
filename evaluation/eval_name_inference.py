import json
import os
import re
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

cluster_dir = "data/cluster-result"
training_result_dir = "data/training-result"
es_path = "data/extend-names/es_meta.csv"

def load_json(json_file):
    if os.path.exists(json_file):
        with open(json_file,"r") as f:
            return json.load(f)
    else:
        return {}

def split_word(word:str):
    if len(word) > 0 and word[0].isnumeric(): return []
    words = word.split("_")
    ret = []
    for w in words:
        w = re.sub("\W","",w)
        ws = re.split("([A-Z][a-z]+)|([A-Z]{2,})|([a-z]{2,})",w)
        ret.extend([wi.lower() for wi in ws if wi is not None and len(wi)>0])
    return ret

def unsplit_words(words:str):
    if len(words) == 0: return ""
    if len(words) == 1: return words[0]
    return "".join([words[0]] + [w.capitalize() for w in words[1:]])

class Evaluator:
    def __init__(self, cluster_result, es_meta_path, label_path, result_file, top_freq:int=100, reforce_run:bool=False) -> None:
        self.result_data = pd.read_csv(result_file, low_memory=False)
        self.label2name = load_json(label_path)

        self.seen_names = set()
        for l, names in self.label2name.items():
            self.seen_names |= set([name[1] for name in names['name_list']])
        self.number_classes = len(self.label2name)
        
        # self.total_data = self.result_data[~self.result_data['unseen_name'].isna()]
        self.total_data = self.result_data[(~self.result_data['unseen_name'].isna()) & (self.result_data['unseen_name'].isin(self.seen_names))]
        self.total_names = len(self.total_data)
    
        self.total_data = self.total_data[self.total_data['data_type'].isin(set(cluster_result[cluster_result['label']>-1]['data_type']))]

        new_result = result_file.replace(".csv","_w_predname.csv")
        
        if not reforce_run and os.path.exists(new_result):
            self.total_data = pd.read_csv(new_result)
        else:
            self.apply_pred_names()
            self.total_data.to_csv(new_result)

        self.total_data['type_name'] = self.total_data['data_type'] + ' ' + self.total_data['unseen_name']
            
        self.word_counts = self.total_data['type_name'].value_counts()
        
        self.es_meta_path = es_meta_path
        
        # top_words = self.word_counts.head(top_freq).index.tolist()
        # self.to_eval_data = self.total_data[self.total_data['type_name'].isin(top_words)]
        self.reset_top_freq(top_freq)
    
    def apply_pred_names(self):
        tqdm.pandas()
        def apply_name(row):
            ret = {'pred_type': self.label2name[str(row['pred@1'])]['name_list'][0][0]}
            for i in range(1,6):
                ret[f'pred_name@{i}'] = self.label2name[str(row[f'pred@{i}'])]['name_list'][0][1]
            return pd.Series(ret)
    
        new_colums = self.total_data.progress_apply(apply_name, axis=1)
        self.total_data[['pred_type'] + [f'pred_name@{i}' for i in range(1,6)]] = new_colums
    
    def reset_top_freq(self, new_top_freq:int):
        if new_top_freq > 0:
            top_words = self.word_counts.head(new_top_freq).index.tolist()
            self.to_eval_data = self.total_data[self.total_data['type_name'].isin(top_words)]
        else:
            self.to_eval_data = self.total_data

        # self.to_eval_data['unseen_name'] = self.to_eval_data['unseen_name'].apply(lambda x:unsplit_words(split_word(x)))
        # self.to_eval_data['pred_name@1'] = self.to_eval_data['pred_name@1'].apply(lambda x:unsplit_words(split_word(x)))
        

    def strict_equal(self) -> float:
        incorrect_pairs = []
        top_values = {i:0 for i in range(1,6)}
        for i, row in self.to_eval_data.iterrows():
            data_type = row['data_type']
            ground_truth = unsplit_words(split_word(row['unseen_name']))
            pred_names = [unsplit_words(split_word(row[f"pred_name@{i}"])) for i in range(1,6)]
            preded = False
            for i in range(1,6):
                if ground_truth in pred_names[:i]:
                    top_values[i] += 1
                    preded = True
            if not preded:
                incorrect_pairs.append((data_type, ground_truth, pred_names[0]))
        return [f"{top_values[i]/len(self.to_eval_data)*100:.2f}" for i in range(1,6)], incorrect_pairs
        
    def semantic_eval(self, common_count:int=40) -> float:
        incorrect_pairs = []
        
        extended_semantics = defaultdict(lambda: defaultdict(list))
        # assert os.path.exists(self.es_meta_path)
        
        with open(self.es_meta_path,"r") as f:
            for line in f:
                line = line.strip("\n")
                type, word, *sims = line.split(",")

                extended_semantics[type][word] = [unsplit_words(w.split(" ")) for w in sims][:common_count]

        top_values = {i:0 for i in range(1,6)}
        for i, row in self.to_eval_data.iterrows():
            data_type = row['data_type']
            ground_truth = unsplit_words(split_word(row['unseen_name']))
            pred_names = [unsplit_words(split_word(row[f"pred_name@{i}"])) for i in range(1,6)]
            preded = False
            for i in range(1,6):
                if len(set(pred_names[:i]) & set(extended_semantics[data_type][" ".join(split_word(ground_truth))])) > 0:
                    top_values[i] += 1
                    preded = True
            if not preded:
                incorrect_pairs.append((data_type, ground_truth, pred_names[0]))
        return [f"{top_values[i]/len(self.to_eval_data)*100:.2f}" for i in range(1,6,2)], incorrect_pairs

def get_eval_result():
    print("="*30+"Summarize the result of name inference"+"="*30)
    cluster_result = pd.read_csv(f"{cluster_dir}/cluster_result.csv")
    result_path = f"{training_result_dir}/training_result.csv"
    eval = Evaluator(cluster_result=cluster_result,es_meta_path=es_path, label_path=f"{cluster_dir}/labels.json", result_file=result_path, reforce_run=True)
       
    stat = []
    
    # here, we evaluate all the names
    for top_freq in tqdm([-1]):
        metrics = {
            "total_names":eval.total_names,
            "classes":eval.number_classes,
        }

        eval.reset_top_freq(top_freq)
        se_pre, _ = eval.semantic_eval()
        
        metrics.update({
            f"number_names":len(eval.to_eval_data),
            "Acc@1":se_pre[0],
            "Acc@3":se_pre[1],
            "Acc@5":se_pre[2]
        })
        
        stat.append(metrics)

    stat = pd.DataFrame(stat)
    stat.to_csv(f"{training_result_dir}/result.csv", index=False)

    print("[Fig.9 Right] Here is the Acc@1,Acc@3 and Acc@5 of name inference:")
    print(stat)
    
    return stat

def effects_of_extend_numbers():
    print("="*30+"Summarize the effect of extend numbers"+"="*30)
    cluster_result = pd.read_csv(f"{cluster_dir}/cluster_result.csv")
    result_path = f"{training_result_dir}/training_result.csv"
    eval = Evaluator(cluster_result=cluster_result,es_meta_path=es_path, label_path=f"{cluster_dir}/labels.json", result_file=result_path, reforce_run=True)
    eval.reset_top_freq(-1)

    stat = []
    
    for common_count in tqdm([1]+list(range(0,50+5,5))):
        metrics = {
            "total_names":eval.total_names,
            "classes":eval.number_classes,
        }

        se_pre, _ = eval.semantic_eval(common_count=common_count)
        
        metrics.update({
            "extend_number": common_count,
            "Acc@1":se_pre[0],
            "Acc@3":se_pre[1],
            "Acc@5":se_pre[2]
        })
        
        stat.append(metrics)
    
    stat = pd.DataFrame(stat)
    stat.to_csv(f"{training_result_dir}/effect_of_extend_numbers.csv", index=False)
    print("[Fig.9] Here is the result for different extend number:")
    print(stat)
    return stat
    
def ablation_study():
    print("="*30+"Summarize the ablation study on name inference"+"="*30)
    result_dirs = [
        f"{training_result_dir}/ablation/cluster-unaware",
        f"{training_result_dir}/ablation/uncluster-unaware",
        f"{training_result_dir}/ablation/cross-entropy",
    ]
    
    stat = []
    
    for result_dir in result_dirs:
        cluster_result = pd.read_csv(f"{result_dir}/cluster_result.csv")
        result_path = f"{result_dir}/training_result.csv"

        eval = Evaluator(cluster_result=cluster_result, es_meta_path=es_path, label_path=f"{result_dir}/labels.json", result_file=result_path,reforce_run=True)
        eval.reset_top_freq(-1)

        metrics = {
            "ablation":result_dir.split("/")[-1],
            "total_names":eval.total_names,
            "classes":eval.number_classes
        }
        
        se_pre, _ = eval.semantic_eval()
        
        metrics.update({
            "Acc@1":se_pre[0],
            "Acc@3":se_pre[1],
            "Acc@5":se_pre[2]
            }
        )
        
        stat.append(metrics)

    stat = pd.DataFrame(stat)
    stat.to_csv(f"{training_result_dir}/ablation_study.csv", index=False)
    print("[Fig.9] Here is the ablation study result:")
    print(stat)
    return stat

if __name__ == "__main__":
    # get_eval_result()
    # effects_of_extend_numbers()

    ablation_study()
