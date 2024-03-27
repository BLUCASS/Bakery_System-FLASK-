from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from controller import UserManagement, ProductManagement

user_bp = Blueprint("users", __name__, template_folder='user_templates')


@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserManagement().signup(name=name, email=email, password=password)
        if not user: 
            flash('Sorry, this email is already in use. Please, try a different one or go to the login page.')
            return render_template('signup.html')
        login_user(user)
        return redirect(url_for('users.main', current_user=current_user))

@user_bp.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserManagement().login(email, password)
        if not user:
            flash('Email or password incorrect. Please try again or go to the Register page.')
            return render_template('login.html')
        login_user(user)
        return redirect(url_for('users.main', current_user=current_user))

@user_bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    elif request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        delete = UserManagement().delete_user(password, confirm_password, current_user)
        if delete:
            flash('User successfully deleted.')
            return redirect(url_for('users.login'))
        flash('The passwords do not match')
        return render_template('delete.html')

@user_bp.route('/main')
@login_required
def main():
    return render_template('main.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@user_bp.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    if request.method == 'GET':
        return render_template('purchase.html')
    elif request.method == 'POST':
        data = request.form
        ProductManagement().purchase(data, current_user.id)
        flash('Products purchases successfully')
        return render_template('purchase.html')

@user_bp.route('/history')
@login_required
def history():
    purchased_products = ProductManagement().get_products(current_user.id)
    return render_template('history.html', purchased_products=purchased_products)

@user_bp.route('/catalog')
@login_required
def catalog():
    return render_template('catalog.html')


