# Eddy: Intelligent EVM-Bytecode Decompiler with High Fidelity of Smart Contract Semantics

![](https://img.shields.io/badge/language-python-brightgreen.svg?style=plastic) ![](https://img.shields.io/badge/version-v0.1-brightgreen.svg?style=plastic)

This repository contains supplementary material for the paper "Eddy: Intelligent EVM-Bytecode Decompiler with High Fidelity of Smart Contract Semantics".

**Note**: 
- Our reversed code and some meta information are also published in https://eddy-artifacts.github.io/Eddy/.
- Due to the large size of the data, we only provide some summarized data, and more detailed data and code will be published after the paper is published.
- Some large files are compressed to `zip` files for uploading to `github`, you can decompress it manually (`Windows`), or run process_large_files.py decompress to decompress it automatically (`Linux`).


This repository is organized as follows.
- `data/`: Datasets and evaluation results (section 6).
  - `contract-dataset/`: Deduplicated contracts sorted by their balance.
  - `contract-complexity/`: Pre-analyzed meta information which indicates whether a contract has `loops` or `struct`-typed variables.
  - `except-dataset/`: Contracts with decompiled code or descriptions.
  - `manual-eval-result/`: Manual verification results for some reversed code.
  - `auto-eval-result/`: Automated evaluation result for a larger dataset.
  - `lifting-result/`: Lifting result from EVM Bytecode.
  - `extend-names/`: Extend names of some state variables for name inference evaluation.
  - `training-result/`: Results of name inference.
  - `eval-result.log`: Evaluation running logs.
- `evaluation/`: Evaluation scripts.
  - `run_eval.py`: Evaluation dispatcher.
  - `get_address.py`: Script to prepare different datasets for different questions.
  - `eval_reversed_code.py`: Script to evaluate the reversed code.
  - `eval_semantic_units_lifting.py`: Script to evaluate semantic units lifting.
  - `eval_name_inference.py`: Script to evaluate the unknown name inference.
  - `eval_scalability.py`: Script to evaluate the scalability of Eddy.
- `requirements.txt`: Some necessary packages.
- `process_large_files.py`: Script to zip and unzip large files.
- `run-eval.sh`: Script for quick evaluation.

The artifacts are tested on `Ubuntu 18.04.6 LTS`.

## Quickstart

Make sure that all the dependency has installed before running:

```cmd
git clone -b main --single-branch https://github.com/Eddy-artifacts/Eddy.git
cd Eddy
pip install -f ./requirements.txt
```

Quick Evaluation
```
bash run-eval.sh
```

How to customized evaluation?
```
Usage: run_eval.py [OPTIONS]

This evaluation artifacts do the following things:
  - [RQ1] Evaluate the quality of reversed code.
  - [RQ2] Evaluate our lifting methods.
  - [RQ3] Evaluate the recovered unknown names of state variables.
  - [RQ4] Evaluate the scalability of Eddy.

Options:
--eval-reversed-code    Run the evaluation of the reversed code.
    --manual-eval       Summarize the manual verification result.
    --auto-eval         Summarize the result on large dataset.
    --compiler-errors   Summarize the compiler errors.
    --codegen-ablation  Summarize the ablation study of different settings.
--eval-lifting          Run the evaluation on semantic units lifting.
    --coverage-eval     Summarize the coverage rate.
    --variables-eval    Summarize the result of variable recognition.
--eval-name-inference   Run the evaluation of unknown name inference.
    --name-inference    Summarize the result of name inference.
    --infer-ablation    Summarize the ablation study on name inference.
--eval-scalability      Run the evaluation of scalability.
    --time-cost         Summarize the time cost of analysis.
    --token-cost        Summarize the token count of prompt.
If you do not pass in any options, you can visit the summarized result in ./data/eval-result.log.
```
For example, `python run_eval.py --eval-reversed-code --manual-eval` will only show the result of manual verification for reversed code.


## Detailed Artifact Description
We will describe various scripts in `./evaluation` used in this artifacts and their ourput.

### `eval_reversed_code.py`

This script evaluates the reversed code manually and automatically. Specifically, it reports the following information:
1. The number of semantic-equal reversed code for different contracts (Solidity, Vyper and New) and inputs (Raw Bytecode, Elipmoc Decompiled Code and our descriptions).
2. The compilable rate of automated generated code.
3. The instructions coverage rate of automated generated code.
4. The average and best result on 5 running times.
5. The summarized compiler errors.
6. The effect of different description. The meanings of some of the abbreviations are as follows:

| use inferred names | from function level | add coding specifications | add state variables layout | abbreviations
| :-: | :-: | :-: | :-: | :-: |
| 0 | 0 | 0 | 0 | description_v0000|
| 1 | 0 | 0 | 0 | description_v0100|
| 1 | 1 | 0 | 0 | description_v1100|
| 1 | 1 | 0 | 1 | description_v1101 (a.k.a LayedDescription)|
| 1 | 1 | 1 | 1 | description_v1111 (a.k.a TemplateDescription)|

### `eval_semantic_units_lifting.py`

This script evaluates our semantic units lifting procedure (Section 3). Specifically, it reports the following information:
1. The coverage of analyzed paths and semantic units compared with original EVM bytecode.
2. The precision and recall of our state variable recognition considering types.
3. The precision and recall of our state variable recognition of decompiled code.
4. The improvement score compared with other tools. 

### `eval_name_inference.py`
This script evaluates the unknown name inference (Section 4). Specifically, it reports the following information:
1. The collected names for private state variables (as ground truth). 
2. The Acc@N of inferred names.
3. The effect of extend numbers, cluster, type informtion and focal loss.


### `eval_scalability.py`

This script evaluates the time and money cost for each contract test by us.
