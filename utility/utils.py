import pandas as pd 
import openpyxl as px
import sys
import os
from datetime import datetime
import importlib
from utility.token_counts import get_token

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

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
    llms = ["llama3", "gemma2"]  # Sostituisci con i nomi effettivi degli LLM disponibili
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
    print("3. Exit")

def system_message(llm):
    sys_message = input("Enter a system prompt:\n")
    run_llm_function(llm,sys_message,"system")

