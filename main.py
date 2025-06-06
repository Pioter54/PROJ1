import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import subprocess
from pathlib import Path
import json
import re
from google.cloud import compute_v1, storage
from google.oauth2 import service_account

# Inicjalizacja klienta LangChain
load_dotenv()
client = ChatOpenAI(
    model="gpt-3.5-turbo-1106",#"gpt-4.1-2025-04-14"
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
                    "required": []
                }
            },
            {
                "name": "delete_machine",
                "description": "Generuje Terraform dla usunięcia VM",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project": {"type": "string"},
                        "zone":    {"type": "string"},
                        "name":    {"type": "string"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "stop_machine",
                "description": "Zatrzymuje VM w GCP",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project": {"type": "string"},
                        "zone":    {"type": "string"},
                        "name":    {"type": "string"}
                    },
                    "required": ["name"]
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
                    "required": []
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

def create_machine(params: dict) -> str:
    src = template_dir / "create_machine.tf"
    tf = src.read_text()

    # Wyszukiwanie aktualnych wartości z szablonu
    def extract_value(pattern):
        match = re.search(pattern, tf)
        return match.group(1) if match else ""

    current_values = {
        "project": extract_value(r'project\s*=\s*"([^"]+)"'),
        "region": extract_value(r'region\s*=\s*"([^"]+)"'),
        "zone": extract_value(r'zone\s*=\s*"([^"]+)"'),
        "name": extract_value(r'name\s*=\s*"([^"]+)"'),
        "machine_type": extract_value(r'machine_type\s*=\s*"([^"]+)"'),
        "image": extract_value(r'image\s*=\s*"debian-cloud/([^"]+)"'),
        "network": extract_value(r'network\s*=\s*"([^"]+)"')
    }

    new_values = {
        "project": params.get("project", current_values["project"]),
        "region": params.get("region", current_values["region"]),
        "zone": params.get("zone", current_values["zone"]),
        "name": f'{params["name"]}-vm' if "name" in params else current_values["name"],
        "machine_type": params.get("machine_type", current_values["machine_type"]),
        "image": f'debian-cloud/{params["image"].lower().replace(" ", "-")}' if "image" in params else f'debian-cloud/{current_values["image"]}',
        "network": params.get("network", current_values["network"])
    }

    replacements = {
        r'project\s*=\s*"[^"]+"':        f'project      = "{new_values["project"]}"',
        r'region\s*=\s*"[^"]+"':         f'region       = "{new_values["region"]}"',
        r'zone\s*=\s*"[^"]+"':           f'zone         = "{new_values["zone"]}"',
        r'name\s*=\s*"[^"]+"':           f'name         = "{new_values["name"]}"',
        r'machine_type\s*=\s*"[^"]+"':   f'machine_type = "{new_values["machine_type"]}"',
        r'image\s*=\s*"[^"]+"':          f'image        = "{new_values["image"]}"',
        r'network\s*=\s*"[^"]+"':        f'network      = "{new_values["network"]}"'
    }

    for pat, repl in replacements.items():
        tf = re.sub(pat, repl, tf)

    out_path = output_dir / "output_create_machine.tf"
    out_path.write_text(tf)
    return tf


def create_bucket(params: dict) -> str:
    src = template_dir / "create_bucket.tf"
    tf = src.read_text()

    def extract_value(pattern):
        match = re.search(pattern, tf)
        return match.group(1) if match else ""

    current_name = extract_value(r'name\s*=\s*"([^"]+)"')
    current_location = extract_value(r'location\s*=\s*"([^"]+)"')
    current_storage_class = extract_value(r'storage_class\s*=\s*"([^"]+)"')

    new_name = f'{params["name"]}-bucket' if "name" in params else current_name
    new_location = params.get("location", current_location)
    new_storage_class = params.get("storage_class", current_storage_class)

    replacements = {
        r'name\s*=\s*"[^"]+"':           f'name          = "{new_name}"',
        r'location\s*=\s*"[^"]+"':       f'location      = "{new_location}"',
        r'storage_class\s*=\s*"[^"]+"':  f'storage_class = "{new_storage_class}"'
    }

    for pat, repl in replacements.items():
        tf = re.sub(pat, repl, tf)

    out_path = output_dir / "output_create_bucket.tf"
    out_path.write_text(tf)
    return tf

def delete_machine(params: dict) -> str:
    src = template_dir / "delete_machine.tf"
    tf = src.read_text()

    def extract_value(pattern):
        match = re.search(pattern, tf)
        return match.group(1) if match else ""

    current_values = {
        "project": extract_value(r'project\s*=\s*"([^"]+)"'),
        "zone": extract_value(r'zone\s*=\s*"([^"]+)"'),
        "name": extract_value(r'name\s*=\s*"([^"]+)"')
    }

    new_values = {
        "project": params.get("project", current_values["project"]),
        "zone": params.get("zone", current_values["zone"]),
        "name": params["name"]
    }

    replacements = {
        r'project\s*=\s*"[^"]+"': f'project = "{new_values["project"]}"',
        r'zone\s*=\s*"[^"]+"':    f'zone    = "{new_values["zone"]}"',
        r'name\s*=\s*"[^"]+"':    f'name    = "{new_values["name"]}"'
    }

    for pat, repl in replacements.items():
        tf = re.sub(pat, repl, tf)

    out_path = output_dir / "output_delete_machine.tf"
    out_path.write_text(tf)
    return tf

def stop_machine(params: dict) -> None:
    project = params.get("project")
    zone = params.get("zone")
    name = params.get("name")

    if not all([project, zone, name]):
        raise ValueError("Missing required parameters: project, zone, and name are required")

    instance_client = compute_v1.InstancesClient()
    operation = instance_client.stop(
        project=project,
        zone=zone,
        instance=name
    )
    operation.result()  # Wait for operation to complete
    return f"VM {name} has been stopped"

# --- Main chat function ---
def chat_with_terraform(prompt: str, llm_api_key: str = None) -> dict:
    if not llm_api_key:
        return {"error": "Nie skonfigurowano klucza API dla LLM. Aby móc korzystać z czatu, należy dodać własny klucz API w ustawieniach projektu."}
    
    client = ChatOpenAI(
        api_key=llm_api_key,
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
                        "required": []
                    }
                },
                {
                    "name": "delete_machine",
                    "description": "Generuje Terraform dla usunięcia VM",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project": {"type": "string"},
                            "zone":    {"type": "string"},
                            "name":    {"type": "string"}
                        },
                        "required": ["name"]
                    }
                },
                {
                    "name": "stop_machine",
                    "description": "Zatrzymuje VM w GCP",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project": {"type": "string"},
                            "zone":    {"type": "string"},
                            "name":    {"type": "string"}
                        },
                        "required": ["name"]
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
                        "required": []
                    }
                }
            ],
            "function_call": "auto"
        }
    )

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
# def execute_terraform(directory="."):
#     try:
#         subprocess.run(["terraform", "init"], cwd=directory, check=True)
#         subprocess.run(["terraform", "plan"], cwd=directory, check=True)
#         subprocess.run(["terraform", "apply", "-auto-approve"], cwd=directory, check=True)
#         return "Kod Terraform został zastosowany."
#     except subprocess.CalledProcessError as e:
#         return f"Błąd podczas wykonywania Terraform: {e}"

def stream_terraform(directory="."):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    process = subprocess.Popen(
        'terraform init && terraform plan && terraform apply -auto-approve',
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        text=True
    )

    important_patterns = [
        r'Terraform.*initialized',
        r'Plan: \d+ to add, \d+ to change, \d+ to destroy',
        r'Creating\.\.\.',
        r'Creation complete.*',
        r'Apply complete!.*',
        r'Error:.*',
        r'google_.*'
    ]

    def is_important(line):
        return any(re.search(p, line) for p in important_patterns)

    for line in process.stdout:
        clean = ansi_escape.sub('', line.strip())
        if is_important(clean):
            if "initialized" in clean:
                yield f"data: ✅ Inicjalizacja zakończona\n\n"
            elif "Plan:" in clean:
                yield f"data: 📝 {clean}\n\n"
            elif "Creating..." in clean:
                yield f"data: 🚀 Tworzenie zasobów...\n\n"
            elif "Creation complete" in clean:
                yield f"data: ✅ Zasób utworzony\n\n"
            elif "Apply complete!" in clean:
                yield f"data: ✅ Zastosowano zmiany: {clean}\n\n"
            elif "Error:" in clean:
                yield f"data: ❌ Błąd: {clean}\n\n"
            elif "will be created" in clean:
                yield f"data: 🛠️ Zasób zostanie stworzony\n\n"
            elif "Still creating..." in clean:
                yield f"data: ⏳ Trwa tworzenie zasobu...\n\n"
            # else:
            #     yield f"data: {clean}\n\n"

def fetch_gcp_resources(project_id: str, keyfile_json: str):
    if not project_id or not keyfile_json:
        return [], []

    creds = service_account.Credentials.from_service_account_info(
        json.loads(keyfile_json)
    )

    # VM-ki
    vm_instances = []
    inst_client = compute_v1.InstancesClient(credentials=creds)
    for zone, resp in inst_client.aggregated_list(project=project_id):
        for inst in getattr(resp, "instances", []):
            vm_instances.append(
                {"name": inst.name,
                 "zone": zone.split("/")[-1],
                 "status": inst.status}
            )

    # Bucket-y
    bucket_names = [
        b.name for b in storage.Client(credentials=creds,
                                       project=project_id).list_buckets()
    ]

    return vm_instances, bucket_names