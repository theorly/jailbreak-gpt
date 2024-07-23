import google.generativeai as genai
import json 
import os

API_KEY = 'AIzaSyBxl4diqQVxlmjjr2Z6nZmx7LEtGdQoAAU'

genai.configure(api_key=API_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


def gemini(prompt, json_file, role = 'user'): 
    chat_history = []
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            chat_history = json.load(f)
    while True: 
        if role == 'system':
            chat_history.append({
                "role": role,
                "content": prompt,
            }) 
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config = generation_config,
                system_instruction = prompt
            )
            chat = model.start_chat(history=[])

            with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_history, f, ensure_ascii=False, indent=4)
            
            # Chiedi all'utente il prossimo prompt
            next_prompt = input("Insert prompt ('exit'): ").strip()
            # Interroga il modello. 

            # Controlla se l'utente vuole uscire
            if next_prompt.lower() == 'exit':
                break
            else:
                prompt = next_prompt
                role = 'user' #reset role

        
        else:
            chat_history.append({
                "role": role,
                "content": prompt,
            }) 

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config = generation_config,
            )

            chat = model.start_chat(history=[])

            response = chat.send_message(prompt)
            print(response.text)
            
            chat_history.append({
                "role": "assistant",
                "content": response.text,
            }) 
            with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(chat.history, f, ensure_ascii=False, indent=4)

            
          
            
    print("Chat saved in", json_file)


