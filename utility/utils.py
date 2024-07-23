import pandas as pd 
import openpyxl as px
import sys
import os
from datetime import datetime
import importlib
from utility.token_counts import get_token


def file_to_dataframe(file_path):
    # Controlla l'estensione del file
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.xlsx':
        # Legge il file Excel e crea un DataFrame
        df = pd.read_excel(file_path, engine='openpyxl', index_col=0)
    elif file_extension.lower() == '.csv':
        # Legge il file CSV e crea un DataFrame
        df = pd.read_csv(file_path, index_col=0)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))
    
    return df

def select_llm(llm_choice):
    llms = ["llama3", "gemma2", "gemini", "claude"]  # Sostituisci con i nomi effettivi degli LLM disponibili
    if llm_choice == "all":
        return llms
    elif llm_choice in llms:
        return [llm_choice]
    else:
        print(f"LLM {llm_choice} non disponibile. Seleziona uno tra {llms} o 'all'.")
        return []

def run_llm_function(llm_name, prompt, role ='user'):
    module_name = llm_name
    try:
        llm_module = importlib.import_module(module_name)
        
        llm_function = getattr(llm_module, llm_name)
        # Chiama la funzione con il prompt
        
        current_dateTime = datetime.now()
        
        json_file_name = f"output/chat_history_{llm_name}_{current_dateTime.day}_{current_dateTime.month}_{current_dateTime.year}_{current_dateTime.hour}.{current_dateTime.minute}.json"
        llm_function(prompt, json_file_name, role)
       
    except ModuleNotFoundError:
        print(f"Modulo {llm_name} non trovato.")
    except AttributeError:
        print(f"Funzione non trovata nel modulo {llm_name}.")



def main_menu():
    print("Select what to do:")
    print("1. Run a LLM -   Run a LLM model with a prompt.")
    print("2. Get token counts  -   Get token counts from a prompt.")
    print("3. Modify LLM options - Modify the options of the LLM model.")
    print("4. Exit")


def modify_llm_options():
    options = {
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 64,
        "max_output_tokens" : 8192
    }

    print("Current parameters:")
    for key, value in options.items():
        print(f"{key}: {value}")

    modify = input("Do you want to modify the options? (y/n): ").strip().lower()
    if modify == 'y':
        for key in options:
            new_value = input(f"Enter new value for {key} (or press enter to keep current value): ").strip()
            #if new_value and key == ['temperature', 'top_p']:
            if new_value:
                if key == 'temperature' or key == 'top_p':
                    options[key] = float(new_value)
                elif key == 'top_k' or key == 'max_output_tokens':
            #elif new_value and key == ['top_k', 'max_output_tokens']:
                    options[key] = int(new_value)
        print("Options for LLM updated to:")
        for key, value in options.items():
            print(f"{key}: {value}")
        
    
    return options

def update_options(llm, options):
    module_name = llm

    try:
        llm_module = importlib.import_module(module_name)
        
        llm_module.options = options
        print(llm_module.options)
       
    except ModuleNotFoundError:
        print(f"Modulo {llm} non trovato.")

    