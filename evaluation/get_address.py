import pandas as pd
import os

address_dir = "data/contract-dataset"

complexity_dir = "data/contract-complexity"
contract_dataset = "data/contract-dataset"
except_contract_dir = "data/except-contracts"

def elipmoc_not_exist_addresses():
    return pd.read_csv(f"{except_contract_dir}/non-elipmoc-cases-1000.csv")['address']

def our_non_description_addresses():
    return pd.read_csv(f"{except_contract_dir}/non-description-cases-1000.csv")['address']

def filter_addresses(dataset, except_addresses_list):
    return dataset[~dataset['address'].isin(except_addresses_list)]
      
def get_solidity_addresses(count:int=1000):
    results = pd.read_csv(f"{contract_dataset}/dedup-0-10000000.csv")
    complexity = pd.read_csv(f"{complexity_dir}/solidity.csv")

    dataset = pd.merge(results, complexity, on='address', how='left')
    dataset = dataset[(dataset['has_source']==1) & (dataset['has_struct_data']==False) & (dataset['has_for_loops']==False)]

    dataset = dataset.head(count)

    return dataset

def get_vyper_addresses(count:int=1000):
    results = pd.read_csv(f"{contract_dataset}/dedup-0-10000000.csv")
    complexity = pd.read_csv(f"{complexity_dir}/vyper.csv")

    dataset = pd.merge(results, complexity, on='address', how='left')
    dataset = dataset[(dataset['has_source']==1) & (dataset['has_struct_data']==False) & (dataset['has_for_loops']==False)]

    dataset = dataset.head(count)

    return dataset

def get_new_addresses(count:int=1000):
    results = pd.read_csv(f"{contract_dataset}/dedup-17999500-18000000.csv")
    complexity = pd.read_csv(f"{complexity_dir}/new.csv")

    dataset = pd.merge(results, complexity, on='address', how='left')
    dataset = dataset[(dataset['has_source']==1) & (dataset['has_struct_data']==False) & (dataset['has_for_loops']==False)]

    dataset = dataset.head(count)

    return dataset

if __name__ == "__main__":
    topN = 200
    except_address_list = list(elipmoc_not_exist_addresses()) + list(our_non_description_addresses())
    address_meta = {
        "solidity": filter_addresses(get_solidity_addresses(topN), except_address_list),
        "vyper": filter_addresses(get_vyper_addresses(topN), except_address_list),
        "new": filter_addresses(get_new_addresses(topN), except_address_list)
    }
    
    print(f"#contracts for verification:{[(k,len(v)) for k,v in address_meta.items()]}")