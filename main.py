import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import subprocess
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

def initialize_langchain():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

def generate_terraform(langchain_client, prompt):
    messages = [
        SystemMessage(content="Jesteś asystentem Terraform. Twoim zadaniem jest generowanie wyłącznie poprawnego kodu Terraform na podstawie podanego polecenia. Każdy wygenerowany kod musi być kompletny i zawierać wszystkie wymagane elementy, w tym co najmniej jeden blok 'network_interface' z siecią 'default' i przypisanym publicznym adresem IP. Nie dodawaj wyjaśnień, wstępu ani dodatkowego tekstu. W odpowiedzi generuj wyłącznie czysty kod Terraform."),
        HumanMessage(content=prompt)
    ]
    response = langchain_client(messages)
    return response.content.strip()

def save_terraform_to_file(terraform_code, file_path="main.tf"):
    with open(file_path, "w") as terraform_file:
        terraform_file.write(terraform_code)
    print(f"Kod Terraform zapisany do pliku: {file_path}")

def execute_terraform(directory="."):
    try:
        subprocess.run(["terraform", "init"], cwd=directory, check=True)
        subprocess.run(["terraform", "plan"], cwd=directory, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=directory, check=True)
        return "Kod Terraform został zastosowany."
    except subprocess.CalledProcessError as e:
        return f"Błąd podczas wykonywania Terraform: {e}"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    client = initialize_langchain()
    user_input = request.json.get('message')
    terraform_query = generate_terraform(client, user_input)
    save_terraform_to_file(terraform_query)
    terraform_result = execute_terraform()
    return jsonify({"response": f"Oto kod, który został zastosowany: {terraform_query}", "terraform_result": terraform_result})

if __name__ == "__main__":
    app.run(debug=True)