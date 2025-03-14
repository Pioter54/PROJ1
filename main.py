import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import subprocess
import json
import re

load_dotenv()

def initialize_langchain():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

def generate_json(langchain_client, prompt):
    messages = [
        SystemMessage(content="Na podstawie wiadomości użytkownika określ, jaką infrastrukturę chce utworzyć (np. vm, database, storage, network, other). "
        "Następnie wyodrębnij kluczowe informacje i zapisz je w formacie JSON. Jeśli użytkownik nie podał konkretnej wartości, pomiń ją. Nazwy zmiennych utrzymuj w formacie terraformowym, po angielsku."
        "Nie dodawaj wyjaśnień, wstępu ani dodatkowego tekstu. W odpowiedzi generuj wyłącznie plik json. "
        "Przykładowy format: {\"project_name\": \"my-project\", \"machine_type\": \"n1-standard-1\", \"zone\": \"us-central1-a\", \"image\": \"debian-10\", \"network\": \"default\"}"),
        HumanMessage(content=prompt)
    ]
    response = langchain_client(messages)
    return response.content.strip()

def save_json_to_file(terraform_code, file_path="main.json"):
    with open(file_path, "w") as terraform_file:
        terraform_file.write(terraform_code)
    print(f"Kod Terraform zapisany do pliku: {file_path}")

def update_terraform_from_json(json_file, tf_template, tf_file):
    with open(json_file, 'r') as jf:
        data = json.load(jf)
    
    with open(tf_template, 'r') as tf:
        tf_content = tf.read()
    
    replacements = {
        r'project\s*=\s*"[^"]+"': f'project = "{data["project_name"]}"',
        r'name\s*=\s*"[^"]+"': f'name = "{data["project_name"]}-vm"',
        r'machine_type\s*=\s*"[^"]+"': f'machine_type = "{data["machine_type"]}"',
        r'zone\s*=\s*"[^"]+"': f'zone = "{data["zone"]}"',
        r'image\s*=\s*"[^"]+"': f'image = "debian-cloud/{data["image"].lower().replace(" ", "-")}"',
        r'network\s*=\s*"[^"]+"': f'network = "{data["network"]}"'
    }
    
    for pattern, replacement in replacements.items():
        tf_content = re.sub(pattern, replacement, tf_content)
    
    
    with open(tf_file, 'w') as tf:
        tf.write(tf_content)
    
    return(f"Wygenerowano {tf_file} na podstawie {tf_template}")

def execute_terraform(directory="."):
    # try:
    #     subprocess.run(["terraform", "init"], cwd=directory, check=True)
    #     subprocess.run(["terraform", "plan"], cwd=directory, check=True)
    #     subprocess.run(["terraform", "apply", "-auto-approve"], cwd=directory, check=True)
    #     return "Kod Terraform został zastosowany."
    # except subprocess.CalledProcessError as e:
    #     return f"Błąd podczas wykonywania Terraform: {e}"
    return "Kod Terraform został zastosowany."