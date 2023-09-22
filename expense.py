
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure database (SQLite for simplicity, replace with a more robust DB in production)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Define the User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database tables
db.create_all()

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', expenses=expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category']
        amount = float(request.form['amount'])
        expense = Expense(description=description, category=category, amount=amount, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)