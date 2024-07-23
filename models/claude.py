import anthropic
import os 
from dotenv import load_dotenv
import json

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
options = {
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 64,
        "max_output_tokens" : 4096
    }


def claude(prompt, json_file, role = 'user'):
    chat_history = []
    hist = []
    skip = False

    # Carica la cronologia della chat se il file JSON esiste già
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            chat_history = json.load(f)

    while True: 
        if role == 'user':
            chat_history.append({
                    "role": role,
                    "content": prompt,
            }) 

            hist.append({
                    "role": role,
                    "content": prompt,
                })
            
            message = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    temperature= options['temperature'],
                    top_p= options['top_p'],
                    top_k= options['top_k'],
                    max_tokens= options['max_output_tokens'],
                    messages = hist
            )

            print(f"Claude: {message.content[0].text}")

            chat_history.append({
            "role": "assistant",
            "content": message.content[0].text
            })

            hist.append({
                "role": "assistant",
                "content": message.content[0].text
                })


            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(chat_history, f, ensure_ascii=False, indent=4)

            next_prompt = input("Next prompt ('exit'): ").strip()


            # Controlla se l'utente vuole uscire
            if next_prompt.lower() == 'exit':
                break
            else:
                prompt = next_prompt
    
        else: 
                if skip == False:
                    chat_history.append({
                            "role": role,
                            "content": prompt,
                    }) 


                next_prompt = input("Next prompt ('exit'): ").strip()

                # Controlla se l'utente vuole uscire
                if next_prompt.lower() == 'exit':
                    break
                else:
                    role = 'user' #reset role
                    skip = True

                chat_history.append({
                    "role": role,
                    "content": next_prompt,
                })

                hist.append({
                    "role": role,
                    "content": next_prompt,
                })

                message = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    temperature= options['temperature'],
                    top_p= options['top_p'],
                    top_k= options['top_k'],
                    max_tokens= options['max_output_tokens'],
                    system=prompt,
                    messages= hist,

                )
                print(f"Claude: {message.content[0].text}")

                chat_history.append({
                "role": "assistant",
                "content": message.content[0].text
                })

                hist.append({
                "role": "assistant",
                "content": message.content[0].text
                })

                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_history, f, ensure_ascii=False, indent=4)

                role = 'system'
        

    print("Chat saved in", json_file)
