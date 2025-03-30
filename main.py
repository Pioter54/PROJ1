import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import subprocess
from pathlib import Path
import json
import re

# Inicjalizacja klienta LangChain
load_dotenv()


def initialize_langchain():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)


# Generowanie pliku JSON na podstawie wiadomości użytkownika
# Można to lekko poprawić żeby generowany plik był bardziej uniwersalny
# Przykładowy prompt: "Stwórz mi najtańszą maszynę gcp, nazwa projektu to modern-rhythm-444518-n9 a obraz maszyny użyj Debian 12, typem maszyny e2-micro, w strefie us-central1-a, z domyślną siecią i publicznym adresem IP."
def generate_json(langchain_client, prompt):
    file_path = './terraform-templates/template.json'

    # Wczytaj przykładowy JSON jako wzór
    with open(file_path, 'r') as json_file:
        example_json = json_file.read()
    messages = [
        {"role": "system",
         "content": f"Na podstawie wiadomości użytkownika określ, jaką infrastrukturę chce utworzyć (np. vm, database, storage). Następnie wypisz tylko potrzebne dane w formacie JSON, bez pustych ani zbędnych pól. Użyj nazw pól zgodnych z Terraformem. Nie dodawaj tekstu ani wyjaśnień, tylko czysty JSON. Przykład formatu (tylko orientacyjnie): {example_json}"},
        {"role": "user", "content": prompt}
    ]

    response = langchain_client.invoke(messages)

    return response.content.strip()


# Zapisywanie JSON do pliku
def save_json_to_file(json_code, file_path="temp/output.json"):
    with open(file_path, "w") as json_file:
        json_file.write(json_code)


# Aktualizacja template Terraform na podstawie pliku JSON i zapisywanie go jako nowu plik
def update_terraform_from_json(json_file, template_folder):
    with open(json_file, 'r') as jf:
        data = json.load(jf)

    operations = data.get("operation", "").split(",")

    for operation in operations:
        tf_template_path = os.path.join(template_folder, f"{operation}.tf")
        tf_output_path = os.path.join("temp", f"output_{operation}.tf")

        if not os.path.exists(tf_template_path):
            print(f"Plik {tf_template_path} nie istnieje, pomijam.")
            continue

        with open(tf_template_path, 'r') as tf:
            tf_content = tf.read()

        replacements = {}

        if operation == "create_machine":
            replacements = {
                r'project\s*=\s*"[^"]+"': f'project = "{data.get("project", "")}"',
                r'name\s*=\s*"[^"]+"': f'name = "{data.get("name", "")}-vm"',
                r'machine_type\s*=\s*"[^"]+"': f'machine_type = "{data.get("machine_type", "")}"',
                r'zone\s*=\s*"[^"]+"': f'zone = "{data.get("zone", "")}"',
                r'image\s*=\s*"[^"]+"': f'image = "debian-cloud/{data.get("image", "").lower().replace(" ", "-")}"',
                r'network\s*=\s*"[^"]+"': f'network = "{data.get("network", "")}"'
            }

        elif operation == "create_bucket":
            replacements = {
                r'name\s*=\s*"[^"]+"': f'name = "{data.get("name", "")}-vm"',
                r'location\s*=\s*"[^"]+"': f'location = "{data.get("location", "")}"',
                r'storage_class\s*=\s*"[^"]+"': f'storage_class = "{data.get("storage_class", "")}"',
            }

        for pattern, replacement in replacements.items():
            tf_content = re.sub(pattern, replacement, tf_content)

        with open(tf_output_path, 'w') as tf:
            tf.write(tf_content)

        return tf_content


# Wykonanie kodu Terraform
# Póki co zakomentowane na potrzeby testów
def execute_terraform(directory="."):
    # try:
    #     subprocess.run(["terraform", "init"], cwd=directory, check=True)
    #     subprocess.run(["terraform", "plan"], cwd=directory, check=True)
    #     subprocess.run(["terraform", "apply", "-auto-approve"], cwd=directory, check=True)
    #     return "Kod Terraform został zastosowany."
    # except subprocess.CalledProcessError as e:
    #     return f"Błąd podczas wykonywania Terraform: {e}"
    return "Kod Terraform został zastosowany."


def load_json_template():
    file_path = './terraform-templates/template.json'
    data = json.loads(Path(file_path).read_text())
    return data
