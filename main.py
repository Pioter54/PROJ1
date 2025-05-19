import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import subprocess
from pathlib import Path
import json
import re

# Inicjalizacja klienta LangChain
load_dotenv()
client = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    temperature=0.2,
    model_kwargs={
        "functions": [
            {
                "name": "create_machine",
                "description": "Generuje Terraform dla VM na podstawie szablonu create_machine.tf",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project":      {"type": "string"},
                        "region":       {"type": "string"},
                        "zone":         {"type": "string"},
                        "name":         {"type": "string"},
                        "machine_type": {"type": "string"},
                        "image":        {"type": "string"},
                        "network":      {"type": "string"}
                    },
                    "required": ["project", "region", "zone", "name"]
                }
            },
            {
                "name": "create_bucket",
                "description": "Generuje Terraform dla GCP bucket na podstawie szablonu create_bucket.tf",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name":          {"type": "string"},
                        "location":      {"type": "string"},
                        "storage_class": {"type": "string"}
                    },
                    "required": ["name", "location"]
                }
            }
        ],
        "function_call": "auto"
    }
)

# Template and output directories
template_dir = Path("./terraform-templates")
output_dir = Path("./temp")
output_dir.mkdir(parents=True, exist_ok=True)

# --- Stub implementations for Terraform generation ---
def create_machine(params: dict) -> str:
    src = template_dir / "create_machine.tf"
    tf = src.read_text()
    replacements = {
        r'project\s*=\s*"[^"]+"':        f'project      = "{params.get("project", "")}"',
        r'region\s*=\s*"[^"]+"':         f'region       = "{params.get("region", "")}"',
        r'zone\s*=\s*"[^"]+"':           f'zone         = "{params.get("zone", "")}"',
        r'name\s*=\s*"[^"]+"':           f'name         = "{params.get("name", "")}-vm"',
        r'machine_type\s*=\s*"[^"]+"':   f'machine_type = "{params.get("machine_type", "")}"',
        r'image\s*=\s*"[^"]+"':          f'image        = "debian-cloud/{params.get("image", "").lower().replace(" ", "-")}"',
        r'network\s*=\s*"[^"]+"':        f'network      = "{params.get("network", "")}"'
    }
    for pat, repl in replacements.items():
        tf = re.sub(pat, repl, tf)
    out_path = output_dir / "output_create_machine.tf"
    out_path.write_text(tf)
    return tf

def create_bucket(params: dict) -> str:
    src = template_dir / "create_bucket.tf"
    tf = src.read_text()
    replacements = {
        r'name\s*=\s*"[^"]+"':           f'name          = "{params.get("name", "")}-bucket"',
        r'location\s*=\s*"[^"]+"':       f'location      = "{params.get("location", "")}"',
        r'storage_class\s*=\s*"[^"]+"':  f'storage_class = "{params.get("storage_class", "")}"'
    }
    for pat, repl in replacements.items():
        tf = re.sub(pat, repl, tf)
    out_path = output_dir / "output_create_bucket.tf"
    out_path.write_text(tf)
    return tf

# --- Main chat function ---
def chat_with_terraform(prompt: str) -> dict:
    messages = [
        {"role": "system", "content": (
            "Jesteś asystentem, który rozumie, kiedy należy wygenerować dane wejściowe do szablonu Terraform "
            "(create_machine lub create_bucket), a kiedy po prostu rozmawiać."
        )},
        {"role": "user", "content": prompt}
    ]
    response = client.invoke(messages)
    func_call = response.additional_kwargs.get("function_call")

    if func_call:
        return {
            "type": func_call.get("name"),
            "params": json.loads(func_call.get("arguments", "{}"))
        }

    return {"response": response.content}

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
    return {"response": response.content}
