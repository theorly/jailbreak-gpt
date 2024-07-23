import argparse
import os
import pandas as pd
import sys
from utility.token_counts import get_token
from utility import utils

# Configura l'URL e la chiave API (modifica con i tuoi dettagli)
#api_url = "http://localhost:11434/api/chat"  # Esempio di URL API

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))


def start(): 
        prompt_df = pd.DataFrame()
        while True:
            utils.main_menu()
            scelta = input("Select what to do: ")
            print("----------------------")

            if scelta == '1':
               
                selected_llms = utils.select_llm(args.llm)
                print(f"Selected LLM: {selected_llms}")
                print("----------------------")
                sys = input("Do you want to enter a system prompt? (y/n): ")
                if sys == "y":
                    for llm in selected_llms:
                        sys_prompt = input(f"Enter a system prompt for {llm}:\n")
                        print("----------------------")
                        utils.run_llm_function(llm, sys_prompt, role='system')
                else: 
                    prompt = input("Enter your prompt: ")
                    print("----------------------")
                    for llm in selected_llms:
                        utils.run_llm_function(llm, prompt)
                        
            elif scelta == '2':
                task = input("Single prompt or file? - Digit 'prompt' for single prompt or 'file' for file: \n")
                if task == "prompt":
                    prompt = input("Enter your prompt: ")
                    print(f"Token counts: {get_token(prompt)}")
                elif task == "file":
                    input_path = input("Insert a prompt file path: ")
                    if(os.path.isfile(input_path)):
                        df = utils.file_to_dataframe(input_path)
                        for prompt in df['text']:
                            print(f"Prompt: \n {prompt}")
                            print(f"Token counts: {get_token(prompt)} \n")
                    else:
                        print("File not found. Retry.")
                        raise FileNotFoundError

            elif scelta == '3':
                selected_llms = utils.select_llm(args.llm)
                print("Modify LLM options...")
                print("----------------------")
                new_options = utils.modify_llm_options()
                for llm in selected_llms:
                    utils.update_options(llm, new_options)

            elif scelta == '4':
                print("----------------------")
                print("Exit...")
                break

            else:
                print("Input error, retry.")



if __name__ == "__main__":
    print("Jailbreak-gpt is starting! \n")
    print("----------------------")

    parser = argparse.ArgumentParser(description="Software for Prompt Engineering. Select a mode to use.")
    parser.add_argument("--mode", choices=["select_llm"], help="Select a particular llm to use (default set to all)")
    parser.add_argument("--llm", type=str,default="all", help="Select a LLM")
    parser.add_argument("--prompt_file", type=str,help="Select a file containing prompts (default set to jailbreak-prompt.xlsx)")
    parser.add_argument("--prompt_id", type=int, help="Select a specific prompt from the file")

    args = parser.parse_args()
    
    if args.mode == "select_llm":

        if args.llm:
            
            selected_llms = utils.select_llm(args.llm)
                
            if args.prompt_file:
                prompt_path = args.prompt_file
                df = utils.file_to_dataframe(prompt_path)
                print("----------------------")
                print(df.head())
                print("----------------------")
                if args.prompt_id:
                    print(f"Selected prompt ID: {args.prompt_id}")
                    prompt = df['text'][args.prompt_id]
                    for llm in selected_llms:
                        utils.run_llm_function(llm, prompt)
                else:
                    for prompt in df['text']:
                        
                        for llm in selected_llms:
                                    print(f"Selected LLM: {selected_llms}")
                                    utils.run_llm_function(llm, prompt)
            else: 
                start()


                
                

    else: 
        start()

