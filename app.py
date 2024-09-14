from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, User, Entry
import secrets
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

secret_key = secrets.token_urlsafe(16)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SECRET_KEY'] = secret_key
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Entering register route")
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Entering login route")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('diary'))
    return render_template('login.html', form=form)

@app.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    print("Entering diary route")
    print(f"Entering diary route. Request method: {request.method}")
    print(f"Request form data: {request.form}")
    if request.method == 'POST':
        new_entry = Entry(content=request.form['content'], user_id=current_user.id)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('diary'))
    
    entries = Entry.query.filter_by(user_id=current_user.id).all()
    return render_template('diary.html', entries=entries)

@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    print("Entering edit entry route")
    entry = Entry.query.get(entry_id)
    if request.method == 'POST':
        entry.content = request.form['content']
        db.session.commit()
        return redirect(url_for('diary'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete_entry/<int:entry_id>')
@login_required
def delete_entry(entry_id):
    print("Entering delete entry route")
    entry = Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('diary'))

@app.errorhandler(Exception)
def handle_error(e):
    print(f"An error occurred: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    return "An error occurred. Please check the server logs for more information.", 500