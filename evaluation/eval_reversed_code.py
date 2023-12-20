import os
from collections import Counter
from tabnanny import verbose
from unittest import result

import numpy as np
import pandas as pd
from scipy import stats

from get_address import (elipmoc_not_exist_addresses, filter_addresses,
                         get_new_addresses, get_solidity_addresses,
                         get_vyper_addresses, our_non_description_addresses)


def manual_eval():
    print("="*30+"Summarize the manual verification result"+"="*30)
    n_solidity = 200
    except_address_list = list(elipmoc_not_exist_addresses()) + list(our_non_description_addresses())
    solidity_addresses = filter_addresses(get_solidity_addresses(n_solidity), except_address_list)
    vyper_addresses = filter_addresses(get_vyper_addresses(n_solidity), except_address_list)
    new_addresses = filter_addresses(get_new_addresses(n_solidity), except_address_list)
    total = pd.concat([solidity_addresses, vyper_addresses, new_addresses], ignore_index=True)
    address_meta = {
        "solidity": solidity_addresses,
        "vyper": vyper_addresses,
        "new": new_addresses,
        "total": total
    }

    # read the manually-verified results
    data = pd.read_csv("data/manual-eval-result/manual_verification_result.csv")
    
    result_summary = []
    for dataset, addresses in address_meta.items():
        for input_type in ["Bytecode", "Elipmoc", "SpecDescription"]:
            # make sure that the generated code is not empty (at least one SAI)
            n_compilable = len(data[(data['address'].isin(addresses['address'])) & (data[f'{input_type}_sai_coverage']>0)])
            n_equivalent = len(data[(data['address'].isin(addresses['address'])) & (data[f'{input_type}_correct']==1)])
            
            result_summary.append({
                "dataset": dataset,
                "input_type": input_type,
                "compilable": f"{n_compilable/len(addresses)*100:.2f}",
                "equivalent": f"{n_equivalent/len(addresses)*100:.2f}",
            })
        
    print("[Fig.6] The result on SC_manual is:")
    result_summary = pd.DataFrame(result_summary)

    # this is the stats for Fig.6
    print(result_summary)
    print()
    print(f"For Bytecode, the semantically equal contracts is {len(data[(data[f'Bytecode_correct']==1)])}")
    print(f"For Elipmoc, the semantically equal contracts is {len(data[(data[f'Elipmoc_correct']==1)])}")
    print(f"For Description, the semantically equal contracts is {len(data[(data[f'SpecDescription_correct']==1)])}")

# compute the error bar
def compute_error_bar(experiment_results, confidence=0.95):
    experiment_results = [float(e) for e in experiment_results]
    assert len(experiment_results) == 5
    mean_value = np.mean(experiment_results)
    std_dev = np.std(experiment_results, ddof=1)
    
    confidence_interval = stats.t.interval(confidence, len(experiment_results) - 1, loc=mean_value, scale=std_dev / np.sqrt(len(experiment_results)))
    error_bar = (confidence_interval[1] - confidence_interval[0]) / 2
    
    return f"{mean_value:.2f}", f"{error_bar:.2f}"

class AutoEval:
    def __init__(self, address_meta, summary_format, sep_times) -> None:
        self.saved_dir = f"data/auto-eval-result/{summary_format}"
        os.makedirs(self.saved_dir, exist_ok=True)

        self.address_meta = address_meta
        self.summary_format = summary_format
                
        summary_path = f"data/auto-eval-result/{summary_format}/sai_coverage_stat.csv"
        self.summary_result = pd.read_csv(summary_path)
        
        self.sep_tims = sep_times

    def get_average_result(self, verbose:bool=False):
        stats = []
        for address_type, address_df in self.address_meta.items():            
            address_list = address_df['address']
            p_compilable_list = []
                        
            n_sai_coverage_list = []
                   
            for i in range(1, 6):
                summary = self.summary_result[(self.summary_result['address'].isin(address_list)) & (self.summary_result['model']==f"{self.summary_format}_{i}")]
                n_prompts = len(summary)
                
                n_compilable = len(summary[(summary['clean_compilable']=='Yes') & (summary['n_sai']>0)])
                sai_coverage = summary['sai_coverage'].mean()
                
                p_compilable_list.append(n_compilable/(n_prompts)*100)

                n_sai_coverage_list.append(f"{sai_coverage*100:.2f}")
                

            p_compilable, e_p_compilable = compute_error_bar(p_compilable_list)

            sai_coverage, e_grammar = compute_error_bar(n_sai_coverage_list)

            stats.append({
                "address_type":address_type,
                "summary_type":self.summary_format,
                
                "#p_compilable":f"{p_compilable}",
                "#e_p_compilable":f"{e_p_compilable}",
                
                "#sai_coverage":f"{sai_coverage}",
                "#e_sai_coverage":f"{e_grammar}",
            })

        stats = pd.DataFrame(stats)    
        stats.to_csv(f"data/auto-eval-result/{self.summary_format}/average_eval.csv", index=False)
        if verbose: print(stats)
        return stats
    
    def get_best_result(self, verbose:bool=False):
        # we assume that the larger the sai_coverage, the better the result
        def choose_row(group):
            return group.loc[group['sai_coverage'].idxmax()]

        self.summary_result['sai_coverage'].fillna(-1, inplace=True)
        best_code = self.summary_result.groupby('address', group_keys=False).apply(choose_row)
                            
        stats = []
        
        for address_type, address_df in self.address_meta.items():
            address_list = address_df['address']
            n_contracts = len(address_list)
            
            summary = best_code[best_code['address'].isin(address_list)]
            
            n_compilable = len(summary[(summary['clean_compilable']=='Yes') & (summary['n_sai'] > 0)])

            selected = summary[summary['sai_coverage']>-1]

            stats.append({
                "summary_type":self.summary_format,
                "address_type":address_type,
                "#compilable":f"{n_compilable/n_contracts*100:.2f}",
                "#sai_coverage":f"{selected['sai_coverage'].mean()*100:.2f}" 
            })

        stats = pd.DataFrame(stats)
        if verbose: print(stats)
        stats.to_csv(f"data/auto-eval-result/{self.summary_format}/best_eval.csv") # save the result
        return stats

def auto_eval(sep_times:bool=False):
    print("="*30+"Summarize the result on large dataset"+"="*30)

    """If sep_times is `true`, we will get the average metrics"""   
    n_solidity = 1000
    
    except_address_list = list(elipmoc_not_exist_addresses()) + list(our_non_description_addresses())
    solidity_addresses = filter_addresses(get_solidity_addresses(n_solidity), except_address_list)
    vyper_addresses = filter_addresses(get_vyper_addresses(n_solidity), except_address_list)
    new_addresses = filter_addresses(get_new_addresses(n_solidity), except_address_list)
    total = pd.concat([solidity_addresses, vyper_addresses, new_addresses], ignore_index=True)
    address_meta = {
        "solidity": solidity_addresses,
        "vyper": vyper_addresses,
        "new": new_addresses,
        "total": total
    }
        
    average_stats = []
    best_stats = []
    for summary_type in ["bytecode", "elipmoc", "description_v1111"]:    
        eval = AutoEval(address_meta, summary_type, sep_times)
        # here, we only use the result on the total dataset, for other results, they can specify the list OR set the verbose to true
        average_result = eval.get_average_result(verbose=False)
        best_result = eval.get_best_result(verbose=False)
        average_stats.append(average_result[average_result['address_type']=="total"])
        best_stats.append(best_result[best_result['address_type']=="total"])
        
    # this is the stats for Fig.7
    average_summary = pd.concat(average_stats, ignore_index=True)
    print(f"[Fig.7 Left] Here is the summary of average result on syntax evaluation for different input:\n {average_summary}")
    best_summary = pd.concat(best_stats, ignore_index=True)
    print(f"[Fig.7 Right] Here is the summary of best result on syntax evaluation for different input:\n {best_summary}")
    
    # eval = AutoEval(address_meta, "description_v1111")
    # eval.get_best_result()

def codegen_ablation():
    print("="*30+"Summarize the ablation study of different settings"+"="*30)
    n_solidity = 1000
    
    except_address_list = list(elipmoc_not_exist_addresses()) + list(our_non_description_addresses())
    solidity_addresses = filter_addresses(get_solidity_addresses(n_solidity), except_address_list)
    vyper_addresses = filter_addresses(get_vyper_addresses(n_solidity), except_address_list)
    new_addresses = filter_addresses(get_new_addresses(n_solidity), except_address_list)
    total = pd.concat([solidity_addresses, vyper_addresses, new_addresses], ignore_index=True)
    address_meta = {
        "solidity": solidity_addresses,
        "vyper": vyper_addresses,
        "new": new_addresses,
        "total": total
    }
    
    ablation_stat = []
    for summary_type in ["description_v1111","description_v1101","description_v1100","description_v0100","description_v0000"]:    
        eval = AutoEval(address_meta, summary_type, sep_times=False)
        best_result = eval.get_best_result(verbose=False)
        ablation_stat.append(best_result[best_result['address_type']=="total"])
        
    # this is the stats for Fig.7
    ablation_summary = pd.concat(ablation_stat, ignore_index=True)
    print(f"[Table 6] Here is the result of ablation study for different descriptions:\n {ablation_summary}")

def summarize_compiler_errors():
    print("="*30+"Summarize the compiler errors"+"="*30)
    compiler_errors = pd.read_csv("data/auto-eval-result/description_v1111/compiler_errors.csv")
    
    print(f"[Tabel 5] Here is the result of summarized top 5 compiler errors:")
    
    for reason, df in compiler_errors.groupby(by='Reasons'):
        print(f"{reason}:{df['Counter'].sum()/compiler_errors['Counter'].sum()*100:.2f}%")
    
    # print(compiler_errors['Reasons'].value_counts())

if __name__ == "__main__":
    print("="*30 + "Here is the result of manual eval resul" + "="*30)
    manual_eval()
    print("="*30 + "Here is the result of auto eval resul" + "="*30)
    auto_eval()
    print("="*30 + "Here is the summarized compiler errors" + "="*30)
    summarize_compiler_errors()
