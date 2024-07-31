#gemma2 model

import requests
import json
import os

url = "http://localhost:11434/api/chat"

options = {}

# Funzione per interagire con il modello Llama3 e salvare i dati in un file JSON
def gemma2(prompt, json_file, role = 'user'):
    chat_history = []

    # Carica la cronologia della chat se il file JSON esiste già
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            chat_history = json.load(f)
        
    else:

        while True:
            # Interrogazione del modello Llama3
           
            # Memorizza l'interazione attuale
            chat_history.append({
                "role" : role,
                "content": prompt,
            })

            response_content = interactive_chat(chat_history)

            chat_history.append({
            "role": "assistant",
            "content": response_content
            })

            # Salva la cronologia aggiornata nel file JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(chat_history, f, ensure_ascii=False, indent=4)

            # Stampa la risposta del modello
            print("gemma2:", response_content)

            # Chiedi all'utente il prossimo prompt
            next_prompt = input("Next prompt ('exit'): ").strip()

            # Controlla se l'utente vuole uscire
            if next_prompt.lower() == 'exit':
                break
            else:
                prompt = next_prompt
                role = 'user' #reset role

        print("Chat salvata in", json_file)

def interactive_chat(chat_history):
    data = {
        "model": "gemma2",
        "messages": chat_history,
        "stream": False,
        "options" : options
        #"format": "json",
    }

    headers = {
        "Content-Type": "application/json"
    }
    

    response = requests.post(url, headers=headers, json=data)
    return response.json()["message"]["content"]