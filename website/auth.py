# for the login, logout and sign up
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Filter the user for the email, and look at the first email (which is unique so there is only one).
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email and password do not match', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='succes')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        birth_date = request.form.get('birthDate')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        creation_date = request.form.get('creation_date')

        user = User.query.filter_by(email=email).first()
        user_check2 = User.query.filter_by(user_name=user_name).first()

        if user:
            flash('Email already exists', category='error')
        elif user_check2:
            flash('Username already exists', category='error')
            print("error")
        elif len(email) < 4:
            flash('Email must be longer than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be longer than 1 character', category='error')
            pass
        elif password1 != password2:
            flash('Passwords do not match', category='error')
            pass
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
            pass
        else:
            # Add the user to the database
            new_user = User(email=email, first_name=first_name, user_name=user_name, last_name=last_name, birth_date=birth_date,
                            password=generate_password_hash(password1, method='sha256'), creation_date=creation_date)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            # flash('Account created', category='succes')
            # when logged in go back to the home page
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


@ login_required
@auth.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        password_ol = request.form.get('password_old')
        password1 = request.form.get('password_new2')
        password2 = request.form.get('password_new2')

        user = User.query.filter_by(email=current_user.email).first()
        if user:
            if check_password_hash(user.password, password_ol):
                if password_ol != password1:
                    if password1 != password2:
                        pass
                    elif len(password1) < 7:
                        flash('Password must be at least 7 characters', category='error')
                        pass
                    else:
                        # Update the user to the database
                        user_update = current_user
                        user_update.password = generate_password_hash(password1, method='sha256')
                        db.session.add(user_update)
                        db.session.commit()
                        login_user(user_update, remember=True)
                        flash('Password updated', category='succes')
                        return redirect(url_for('auth.account'))
                else:
                    flash('Passwords are the same', category='error')

            else:
                flash('Old password incorrect', category='error')
    return render_template("account.html", user=current_user)
