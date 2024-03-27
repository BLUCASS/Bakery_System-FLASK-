from flask import Flask, render_template, redirect, url_for
from database import db
from user import user_bp
from flask_migrate import Migrate
from models import User
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'test_key_2024' # THIS IS THE SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # GIVING THE PATH TO THE DB
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False # SPARING MEMORY
db.init_app(app) # LINKING THE APP WITH THE DATABASE
migrate = Migrate(app, db)

app.register_blueprint(user_bp, url_prefix='/user') # REGISTERING THE BLUEPRINTS

# SETTING THE CONFIGURATIONS FOR THE LOGIN USER
login_manager = LoginManager() # CREATING THE INSTANCE
login_manager.login_view = 'users.login' # THIS WILL REDIRECT ANY UNAUTHORIZED USER TO THAT PAGE
# THE NAME MUST BE THE BLUEPRINT'S NAME
login_manager.init_app(app) # LINKING THE APP


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/products/croissant')
def croissant():
    return render_template('croissant.html')

@app.route('/products/danish')
def danish():
    return render_template('danish.html')

@app.route('/products/choc_swiss')
def choc_swiss():
    return render_template('choc_swiss.html')

@app.route('/products/croissandwich')
def croissandwich():
    return render_template('croissandwich.html')

@app.route('/products/pain')
def pain():
    return render_template('pain.html')

@app.route('/products/sausage')
def sausage():
    return render_template('sausage.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')



if __name__ == '__main__':
    app.run(debug=True)