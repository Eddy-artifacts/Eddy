import pandas as pd

result_dir = "data/lifting-result"

def compute_semantic_units_coverage():
    print("="*30+"Summarize the coverage rate"+"="*30)
    # our results
    stats = []
    result = pd.read_csv(f"{result_dir}/lifting_result_wo_memory_analysis.csv", low_memory=False)
    success = result[(result[f'covered_metrics_operands_operants_static_result']>=0) & (result[f'covered_metrics_operands_operants_dynamic_result']>=0) & (result[f'covered_metrics_operands_operants_fused_result']>=0)]
    
    success_covered = success[f'covered_metrics_operands_operants_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    success_completeness = success[f'completeness_metrics_operands_operants_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"Ethersolve",
        f"#path_coverage":f"{success_covered*100:.2f}",
        f"#semantic_unit_coverage":f"{success_completeness*100:.2f}",
    })

    result = pd.read_csv(f"{result_dir}/lifting_result.csv", low_memory=False)
    
    success = result[(result[f'covered_metrics_operands_operants_static_result']>=0) & (result[f'covered_metrics_operands_operants_dynamic_result']>=0) & (result[f'covered_metrics_operands_operants_fused_result']>=0)]
    
    success_covered = success[f'covered_metrics_operands_operants_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    success_completeness = success[f'completeness_metrics_operands_operants_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"Eddy",
        f"#path_coverage":f"{success_covered*100:.2f}",
        f"#semantic_unit_coverage":f"{success_completeness*100:.2f}",
    })
    
    
    success_covered = success[f'covered_metrics_operands_operants_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    success_completeness = success[f'completeness_metrics_operands_operants_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"wo Memory Analysis",
        f"#path_coverage":f"{success_covered*100:.2f}",
        f"#semantic_unit_coverage":f"{success_completeness*100:.2f}",
    })
    
    result = pd.read_csv(f"{result_dir}/lifting_result_wo_memory_analysis.csv", low_memory=False)
    success = result[(result[f'covered_metrics_operands_operants_static_result']>=0) & (result[f'covered_metrics_operands_operants_dynamic_result']>=0) & (result[f'covered_metrics_operands_operants_fused_result']>=0)]
    
    success_covered = success[f'covered_metrics_operands_operants_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    success_completeness = success[f'completeness_metrics_operands_operants_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"wo Transaction",
        f"#path_coverage":f"{success_covered*100:.2f}",
        f"#semantic_unit_coverage":f"{success_completeness*100:.2f}",
    })

    stats = pd.DataFrame(stats)
    # stats.to_csv(f"{result_dir}/cc_{version}.csv", index=False)
    stats.to_csv(f"{result_dir}/semantic_units_results.csv", index=False)
    print("[Table 7] Here is the result of semantic unit extraction:")
    print(stats)
    return stats

def eval_state_variables():
    print("="*30+"Summarize the result of variable recognition"+"="*30)
    # our results
    result = pd.read_csv(f"{result_dir}/lifting_result.csv", low_memory=False)
    
    stats = []
    
    success = result[(result[f'our_wo_p_metrics_evm_state_recovey_static_result']>=0) & (result[f'our_wo_p_metrics_evm_state_recovey_dynamic_result']>=0) & (result[f'our_wo_p_metrics_evm_state_recovey_fused_result']>=0) & (result[f'lib_wo_p']>=0)]

    
    lib_wo_p = success[f'lib_wo_p'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    lib_wo_r = success[f'lib_wo_r'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    lib_w_p = success[f'lib_w_p'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    lib_w_r = success[f'lib_w_r'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"elipmoc",
        f"#precision":f"{lib_w_p*100:.2f}",
        f"#recall":f"{lib_w_r*100:.2f}",
        f"#wo_type_precision":f"{lib_wo_p*100:.2f}",
        f"#wo_type_recall":f"{lib_wo_r*100:.2f}",
    })
    
    wo_p = success[f'our_wo_p_metrics_evm_state_recovey_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    wo_r = success[f'our_wo_r_metrics_evm_state_recovey_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    w_p = success[f'our_w_p_metrics_evm_state_recovey_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    w_r = success[f'our_w_r_metrics_evm_state_recovey_fused_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"Eddy",
        f"#precision":f"{w_p*100:.2f}",
        f"#recall":f"{w_r*100:.2f}",
        f"#wo_type_precision":f"{wo_p*100:.2f}",
        f"#wo_type_recall":f"{wo_r*100:.2f}",
    })

    
    # success = analysis_result[analysis_result[f'covered_metrics_operands_operants_{result}']>=0]
    wo_p = success[f'our_wo_p_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    wo_r = success[f'our_wo_r_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    w_p = success[f'our_w_p_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    w_r = success[f'our_w_r_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"wo Memory Analysis",
        f"#precision":f"{w_p*100:.2f}",
        f"#recall":f"{w_r*100:.2f}",
        f"#wo_type_precision":f"{wo_p*100:.2f}",
        f"#wo_type_recall":f"{wo_r*100:.2f}",
    })
    
    result = pd.read_csv(f"{result_dir}/lifting_result_wo_memory_analysis.csv", low_memory=False)
    success = result[(result[f'our_wo_p_metrics_evm_state_recovey_static_result']>=0) & (result[f'our_wo_p_metrics_evm_state_recovey_dynamic_result']>=0) & (result[f'our_wo_p_metrics_evm_state_recovey_fused_result']>=0) & (result[f'lib_wo_p']>=0)]
    
    wo_p = success[f'our_wo_p_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    wo_r = success[f'our_wo_r_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    w_p = success[f'our_w_p_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()
    w_r = success[f'our_w_r_metrics_evm_state_recovey_static_result'].fillna(0).apply(lambda x:0 if x<=0 else x).mean()

    stats.append({
        "type":"wo Transactions",
        f"#precision":f"{w_p*100:.2f}",
        f"#recall":f"{w_r*100:.2f}",
        f"#wo_type_precision":f"{wo_p*100:.2f}",
        f"#wo_type_recall":f"{wo_r*100:.2f}",
    })
    
    stats = pd.DataFrame(stats)
    stats.to_csv(f"{result_dir}/state_variables_analysis_result.csv", index=False)
    print("[Table 7] Here is the result of state variables recognition:")
    print(stats)
    return stats

if __name__ == "__main__":
    # compute_semantic_units_coverage()
    eval_state_variables()