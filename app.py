from main import initialize_langchain, generate_terraform, save_terraform_to_file, execute_terraform
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

app.run(debug=True, host='0.0.0.0', port=5000)