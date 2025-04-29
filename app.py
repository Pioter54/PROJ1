# app.py
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from main import initialize_langchain, generate_json, save_json_to_file, update_terraform_from_json, execute_terraform
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    project_name = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=True)

with app.app_context():
    db.create_all()

# Decorator do sprawdzania autentykacji
def login_required(f):
    @wraps(f)  # Dodaj ten dekorator
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('chat.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['project_name'] = user.project_name
            session['location'] = user.location
            return redirect(url_for('index'))
        return render_template('login.html', error='Nieprawidłowy login lub hasło')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Użytkownik już istnieje')
            
        new_user = User(
            username=username,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'], endpoint='chat_endpoint')
@login_required
def chat():
    client = initialize_langchain()
    user_input = request.json.get('message')
    project_name = session.get('project_name', '')
    location = session.get('location', '')
    prompt = f"{user_input} moje szczegóły: project:{project_name}, location:{location}"
    print(f"Prompt: {prompt}")
    generated_json = generate_json(client, prompt)
    # Zwracamy JSON do wyświetlenia użytkownikowi
    return jsonify({"json_code": generated_json})

@app.route('/approve_json', methods=['POST'], endpoint='approve_json_endpoint')
@login_required
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        new_project = request.form['project_name']
        new_location = request.form['location']
        
        # Sprawdź unikalność nazwy użytkownika
        if User.query.filter(User.username == new_username, User.id != user.id).first():
            return render_template('profile.html', 
                                 user=user, 
                                 error='Nazwa użytkownika jest już zajęta')
        
        # Aktualizuj dane
        user.username = new_username
        user.project_name = new_project
        user.location = new_location
        
        if new_password:
            user.password = generate_password_hash(new_password)
        
        db.session.commit()

        session['project_name'] = new_project
        session['location'] = new_location

        return redirect(url_for('profile', success='Dane zostały zaktualizowane'))
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)