from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from main import chat_with_terraform,stream_terraform,fetch_gcp_resources
from flask import flash,Response 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default="")
    location = db.Column(db.String(250), default="")
    zone = db.Column(db.String(250), default="")
    active = db.Column(db.Boolean, default=False)
    machine_type = db.Column(db.String(250), default="")
    google_cloud_keyfile_json = db.Column(db.String(1000), default="")
    llm_api_key = db.Column(db.String(250), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('projects', lazy=True))

with app.app_context():
    db.create_all()

# Decorator do sprawdzania autentykacji
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    user    = User.query.get(session['user_id'])
    project = Project.query.filter_by(user_id=user.id, active=True).first()
    return render_template('chat.html', project=project)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
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

@app.route('/chat', methods=['POST'])
@login_required
def chat_endpoint():
    user_input  = request.json.get('message', '')
    project_name = session.get('project_name', '')
    location     = session.get('location', '')
    zone         = session.get('zone', '')
    machine_type = session.get('machine_type', '')
    llm_api_key  = session.get('llm_api_key', '')
    
    if not llm_api_key:
        return jsonify({
            "error": "Nie skonfigurowano klucza API dla LLM. Aby móc korzystać z czatu, należy dodać własny klucz API w ustawieniach projektu."
        })
    
    prompt = f"{user_input} moje szczegóły: project:{project_name}, location:{location}, zone:{zone,}, machine_type:{machine_type}"
    result = chat_with_terraform(prompt, llm_api_key)
    return jsonify(result)

@app.route('/generate_tf', methods=['POST'])
@login_required
def generate_tf():
    data = request.json
    type_ = data.get('type')
    params = data.get('params', {})

    if type_ == "create_machine":
        from main import create_machine
        tf_output = create_machine(params)
    elif type_ == "delete_machine":
        from main import delete_machine
        tf_output = delete_machine(params)
    elif type_ == "stop_machine":
        from main import stop_machine
        try:
            result = stop_machine(params)
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    elif type_ == "create_bucket":
        from main import create_bucket
        tf_output = create_bucket(params)
    else:
        return jsonify({'result': 'Nieobsługiwany typ zasobu.'})

    return jsonify({'result': tf_output})

@app.route('/stream_apply_tf')
@login_required
def stream_apply_tf():
    def generate():
        yield from stream_terraform(directory='./temp')
    return Response(generate(), mimetype='text/event-stream')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    project = Project.query.filter_by(user_id=user.id, active=True).first()
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        new_project  = request.form['project_name']
        new_location = request.form['location']
        new_zone    = request.form['zone']
        new_machine_type = request.form['machine_type']
        if User.query.filter(User.username == new_username, User.id != user.id).first():
            return render_template('profile.html', user=user, error='Nazwa użytkownika jest już zajęta')
        user.username     = new_username
        project.name = new_project
        project.location = new_location
        project.zone = new_zone
        project.machine_type = new_machine_type
        if new_password:
            user.password = generate_password_hash(new_password)
        db.session.commit()
        session['project_name'] = new_project
        session['location']     = new_location
        session['zone']         = new_zone
        session['machine_type'] = new_machine_type
        return redirect(url_for('profile', success='Dane zostały zaktualizowane'))
    vm_instances, gcs_buckets = fetch_gcp_resources(
        project.name if project else None,
        project.google_cloud_keyfile_json if project else None
    )
    print(">>> vm_instances =", vm_instances)
    print(">>> gcs_buckets =", gcs_buckets)

    return render_template(
        'profile.html',
        user=user,
        project=project,
        vm_instances=vm_instances,
        gcs_buckets=gcs_buckets
    )

@app.route("/create_project", methods=["POST"])
@login_required
def create_project():
    name = request.form.get("project_name")
    location = request.form.get("location")
    zone = request.form.get("zone")
    machine_type = request.form.get("machine_type")
    google_cloud_keyfile_json = request.form.get("google_cloud_keyfile_json", "")
    llm_api_key = request.form.get("llm_api_key", "")
    if name and location:
        new_project = Project(
            name=name,
            location=location,
            zone=zone,
            machine_type=machine_type,
            user_id=session['user_id'],
            google_cloud_keyfile_json=google_cloud_keyfile_json,
            llm_api_key=llm_api_key
        )
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for("profile"))

@app.route("/toggle_project/<int:project_id>", methods=["POST"])
@login_required
def toggle_project(project_id):
    user_id = session['user_id']

    Project.query.filter_by(user_id=user_id, active=True).update({Project.active: False})
    
    project = Project.query.filter_by(id=project_id, user_id=user_id).first_or_404()
    project.active = True
    db.session.commit()
    session['project_name'] = project.name
    session['location'] = project.location
    session['zone'] = project.zone
    session['machine_type'] = project.machine_type
    session["google_cloud_keyfile_json"] = project.google_cloud_keyfile_json
    if project.google_cloud_keyfile_json:
        os.environ["GOOGLE_CREDENTIALS"] = project.google_cloud_keyfile_json

    print("Ustawiam sesję:")
    print("project_name =", project.name)
    print("location =", project.location)
    print("zone =", project.zone)
    print("machine_type =", project.machine_type)
    print("google_cloud_keyfile_json =", project.google_cloud_keyfile_json)

    return jsonify({"status": "ok", "active": True})

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    user = User.query.get(session['user_id'])
    project = Project.query.filter_by(id=project_id, user_id=user.id).first_or_404()

    if request.method == 'POST':
        project.name          = request.form['project_name']
        project.location      = request.form['location']
        project.zone          = request.form['zone']
        project.machine_type  = request.form['machine_type']
        project.google_cloud_keyfile_json   = request.form.get('google_cloud_keyfile_json', '')
        project.llm_api_key   = request.form.get('llm_api_key', '')
        db.session.commit()

        if project.active:
            session['project_name'] = project.name
            session['location']     = project.location
            session['zone']         = project.zone
            session['machine_type'] = project.machine_type
            session['google_cloud_keyfile_json'] = project.google_cloud_keyfile_json
            session['llm_api_key'] = project.llm_api_key

        return redirect(url_for('profile'))

    return render_template('edit_project.html', project=project)


@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first_or_404()
    
    db.session.delete(project)
    db.session.commit()

    if session.get('project_name') == project.name:
        session.pop('project_name', None)
        session.pop('location', None)
        session.pop('zone', None)
        session.pop('machine_type', None)

    flash(f"Projekt \"{project.name}\" został usunięty.")
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
