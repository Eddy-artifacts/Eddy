import sys

from eval_reversed_code import manual_eval, auto_eval, codegen_ablation, summarize_compiler_errors
from eval_semantic_units_lifting import compute_semantic_units_coverage, eval_state_variables
from eval_name_inference import get_eval_result, effects_of_extend_numbers, ablation_study
from eval_scalability import compute_average_time_cost, compute_token_stat

def help_message(): 
    print("Usage: run_eval.py [OPTIONS]")
    print("")
    print("This evaluation artifacts do the following things:")
    print("  - [RQ1] Evaluate the quality of reversed code.")
    print("  - [RQ2] Evaluate our lifting methods.")
    print("  - [RQ3] Evaluate the recovered unknown names of state variables.")
    print("  - [RQ4] Evaluate the scalability of Eddy.")
    print("")
    print("Options:")
    print("--eval-reversed-code    Run the evaluation of the reversed code.")
    print("    --manual-eval       Summarize the manual verification result.")
    print("    --auto-eval         Summarize the result on large dataset.")
    print("    --compiler-errors   Summarize the compiler errors.")
    print("    --codegen-ablation  Summarize the ablation study of different settings.")
    print("--eval-lifting          Run the evaluation on semantic units lifting.")
    print("    --coverage-eval     Summarize the coverage rate.")
    print("    --variables-eval    Summarize the result of variable recognition.")
    print("--eval-name-inference   Run the evaluation of unknown name inference.")
    print("    --name-inference    Summarize the result of name inference.")
    print("    --infer-ablation    Summarize the ablation study on name inference.")
    print("--eval-scalability      Run the evaluation of scalability.")
    print("    --time-cost         Summarize the time cost of analysis.")
    print("    --token-cost        Summarize the token count of prompt.")
    print("If you do not pass in any options, you can visit the summarized result in ./data/eval-result.log.")

def main():
    args = sys.argv[1:]
    if len(args)==0 or args[0] == "-h" or args[0] == "--help": 
        help_message()
        sys.exit()

    if args[0] == "--eval-reversed-code":
        if len(args) > 1:
            for arg in args[1:]:
                if arg == "--manual-eval":
                    manual_eval()
                elif arg == "--auto-eval":
                    auto_eval()
                elif arg == "--compiler-errors":
                    summarize_compiler_errors()
                elif arg == "--codegen-ablation":
                    codegen_ablation()
                else:
                    help_message()
                    sys.exit()
        else:
            print("*"*30+"Run the evaluation of the reversed code."+"*"*30)
            manual_eval()
            auto_eval()
            summarize_compiler_errors()
            codegen_ablation()
            
    elif args[0] == "--eval-lifting":
        if len(args) > 1:
            for arg in args[1:]:
                if arg == "--coverage-eval":
                    compute_semantic_units_coverage()
                elif args == "--variables-eval":
                    eval_state_variables()
                else:
                    help_message()
                    sys.exit()
        else:
            print("*"*30+"Run the evaluation on semantic units lifting."+"*"*30)
            compute_semantic_units_coverage()
            eval_state_variables()
            
    elif args[0] == "--eval-name-inference":
        if len(args) > 1:
            for arg in args[1:]:
                if arg == "--name-inference":
                    get_eval_result()
                elif args == "--infer-ablation":
                    effects_of_extend_numbers()
                    ablation_study()
                else:
                    help_message()
                    sys.exit()
        else:
            print("*"*30+"Run the evaluation of unknown name inference."+"*"*30)
            get_eval_result()
            effects_of_extend_numbers()
            ablation_study()
    
    elif args[0] == "--eval-scalability":
        if len(args) > 1:
            for arg in args[1:]:
                if arg == "--time-cost":
                    compute_average_time_cost()
                elif args == "--token-cost":
                    compute_token_stat()
                else:
                    help_message()
                    sys.exit()
        else:
            print("*"*30+"Run the evaluation of scalability."+"*"*30)
            compute_average_time_cost()
            compute_token_stat()
    else:
        help_message()
        sys.exit()
            
if __name__ == "__main__":
    main()    # dispatch evaluation