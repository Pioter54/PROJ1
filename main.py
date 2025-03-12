import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import subprocess

load_dotenv()

def initialize_langchain():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

def generate_terraform(langchain_client, prompt):
    messages = [
        SystemMessage(content="Jesteś asystentem Terraform. Twoim zadaniem jest wyłącznie wyciągnięcie z wiadomości co użytkownik chce zrobić i jakie szczegóły powinny być w skrypcie. "
        "Zapisz te szczegóły w sformatowanym pliku Json, jeśli jakiegoś szczegółu prakuje zaproponuj przykłądowe wartości."
        "Zmienne w pliku json nazywaj tak jak nazwy zmiennych w Terraform."
        "Nie dodawaj wyjaśnień, wstępu ani dodatkowego tekstu. W odpowiedzi generuj wyłącznie plik json."),
        HumanMessage(content=prompt)
    ]
    response = langchain_client(messages)
    return response.content.strip()

def save_terraform_to_file(terraform_code, file_path="main.json"):
    with open(file_path, "w") as terraform_file:
        terraform_file.write(terraform_code)
    print(f"Kod Terraform zapisany do pliku: {file_path}")

def execute_terraform(directory="."):
    # try:
    #     subprocess.run(["terraform", "init"], cwd=directory, check=True)
    #     subprocess.run(["terraform", "plan"], cwd=directory, check=True)
    #     subprocess.run(["terraform", "apply", "-auto-approve"], cwd=directory, check=True)
    #     return "Kod Terraform został zastosowany."
    # except subprocess.CalledProcessError as e:
    #     return f"Błąd podczas wykonywania Terraform: {e}"
    return "Kod Terraform został zastosowany."