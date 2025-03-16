from main import initialize_langchain, generate_json, save_json_to_file, update_terraform_from_json, execute_terraform
from flask import Flask, render_template, request, jsonify

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    client = initialize_langchain()
    user_input = request.json.get('message')
    json = generate_json(client, user_input)
    save_json_to_file(json)
    terraform_query = update_terraform_from_json("main.json", "terraform-templates/create_machine.tf", "main.tf")
    terraform_result = execute_terraform()
    return jsonify({"response": f"Oto kod, który został zastosowany: {terraform_query}", "terraform_result": terraform_result})

app.run(debug=True, host='0.0.0.0', port=5000)