import pandas as pd

def compute_average_time_cost():
    print("="*30+"Summarize the time cost of analysis"+"="*30)
    result = pd.read_csv("data/lifting-result/static_time_stat.csv")
    print(f"Average for static analysis is {result['time_execution'].mean():.2f}s")
    result = pd.read_csv("data/lifting-result/dynamic_time_stat.csv")
    print(f"Average for dynamic analysis is {result['time_execution'].mean():.2f}s")

def compute_token_stat():
    print("="*30+"Summarize the token count of prompt"+"="*30)
    # https://openai.com/pricing
    result = pd.read_csv("data/auto-eval-result/description_v1111/token_stat.csv")
    
    average_input_token = result['prompt_tokens'].mean()
    average_output_token = result['completion_tokens'].mean()
    average_cost = average_input_token/1000 * 0.06 + average_output_token/1000 * 0.12
    print(f"Average input token is {average_input_token:.2f}")
    print(f"Average output token is {average_output_token:.2f}")
    print(f"Average cost {average_input_token:2f}/1k*0.06+{average_output_token:2f}/1k*0.12=${average_cost:.2f}") 
    
if __name__ == "__main__":
    # compute_average_time_cost()
    
    compute_token_stat()