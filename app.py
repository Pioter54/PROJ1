# app.py
from main import initialize_langchain, generate_json, save_json_to_file, update_terraform_from_json, execute_terraform
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    client = initialize_langchain()
    user_input = request.json.get('message')
    generated_json = generate_json(client, user_input)
    # Zwracamy JSON do wyświetlenia użytkownikowi
    return jsonify({"json_code": generated_json})


@app.route('/approve_json', methods=['POST'])
def approve_json():
    approved_json = request.json.get('json_code')
    # Zapisujemy zatwierdzony JSON do pliku
    save_json_to_file(approved_json)
    terraform_query = update_terraform_from_json("temp/output.json", "terraform-templates")
    terraform_result = execute_terraform()
    return jsonify({
        "response": f"{terraform_query}",
        "terraform_result": terraform_result
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
