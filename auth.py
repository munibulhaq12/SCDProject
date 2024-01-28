from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


# Sample users (for demonstration purposes, you should use a database in a real application)
users = [
    User(1, 'user1', 'password1'),
    User(2, 'user2', 'password2')
]

# File upload setup
uploads = UploadSet('uploads', IMAGES)
app.config['UPLOADED_FILES_DEST'] = 'static/uploads'
configure_uploads(app, uploads)


# Routes
@app.route('/')
@login_required
def index():
    return f'Hello, {current_user.username}!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user.username == username and user.password == password), None)

        if user:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file:
            filename = uploads.save(file)
            return f'File uploaded: {filename}'

    return render_template('upload.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
