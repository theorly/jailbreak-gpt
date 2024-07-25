import google.generativeai as genai
from dotenv import load_dotenv
import json 
import os

# Carica le variabili d'ambiente dal file .env

load_dotenv()

# Ottieni la chiave API dalla variabile d'ambiente
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

options = {}

def gemini(prompt, json_file, role = 'user'): 
    chat_history = []
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            chat_history = json.load(f)
    
    if role == 'user':
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config = options,
            )
            skip = True
    else: 
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config = options,
                system_instruction = prompt
            )
            chat_history.append({
                "role": role,
                "content": prompt,
            }) 
            skip = False
            role = 'user'
    
    chat = model.start_chat(history=[])
    
    
    # write in the json if there is a system instruction 
    with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)

    while True: 
            
        if skip == False: 
            # Chiedi all'utente il prossimo prompt
            next_prompt = input("Insert prompt ('exit'): ").strip()
            # Interroga il modello.
        else: 
            next_prompt = prompt
            skip = False

        
        # Controlla se l'utente vuole uscire
        if next_prompt.lower() == 'exit':
            break
        else:
            chat_history.append({
                "role": role,
                "content": next_prompt,
            })  

            response = chat.send_message(next_prompt)
            print(f"Gemini:{response.text}")

            chat_history.append({
                        "role": 'assistant',
                        "content": response.text,
                    }) 

            with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_history, f, ensure_ascii=False, indent=4)

            
    print("Chat saved in", json_file)


