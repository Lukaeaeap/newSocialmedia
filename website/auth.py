# for the login, logout and sign up
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

'''Error messages English'''
'''
# Loggin in
wrong_password = 'Incorrect password, try again.'
no_match = 'Email and password do not match.'
logged_in = 'Logged in!'

# Logout
logged_out = 'Logged out successfully!'

# Signing up
email_exists = 'Email already exists.'
username_exists = 'Username already exists.'
email_short = 'Email must be longer than 4 characters.'
firstname_short = 'First name must be longer than 1 character.'
password_no_match = 'Passwords do not match.'
password_short = 'Password must be at least 7 characters.'
created_account = 'Account created'

# Changing password
new_password_short = 'New password must be at least 7 characters.'
same_password = 'Old and new passwords are the same.'
password_old_wrong = 'Old password incorrect.'
update_pass_succes = 'Password updated succesfully.'
'''

'''Error messages Dutch'''
# Loggin in
wrong_password = 'Uw wachtwoord is verkeerd.'
no_match = 'Uw mail of wachtwoord klopt niet.'
logged_in = 'Ingelogd!'

# Logout
logged_out = 'Succesvol uitgelogd!'

# Signing up
email_exists = 'Email bestaat al.'
username_exists = 'Gebruikersnaam bestaat al.'
email_short = 'Email moet langer dan 4 karakters zijn.'
firstname_short = 'Voornaam moet langer dan 1 karakter zijn.'
password_no_match = 'Wachtwoorden komen niet overeen.'
password_short = 'Wachtwoord moet minstens 7 karakters lang zijn.'
created_account = 'Account aangemaakt'

# Changing password
new_password_short = 'Het nieuwe wachtwoord moet minstens 7 karakters lang zijn.'
same_password = 'Het oude en nieuwe wachtwoord zijn hetzelfde.'
password_old_wrong = 'Het oude wachtwoord is incorrect.'
update_pass_succes = 'Wachtwoord succesvol geüpdate.'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Filter the user for the email, and look at the first email (which is unique so there is only one).
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash(logged_in, category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(wrong_password, category='error')
        else:
            flash(no_match, category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(logged_out, category='succes')
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
            flash(email_exists, category='error')
        elif user_check2:
            flash(username_exists, category='error')
        elif len(email) < 4:
            flash(email_short, category='error')
        elif len(first_name) < 2:
            flash(firstname_short, category='error')
            pass
        elif password1 != password2:
            flash(password_no_match, category='error')
            pass
        elif len(password1) < 7:
            flash(password_short, category='error')
            pass
        else:
            # Add the user to the database
            new_user = User(email=email, first_name=first_name, user_name=user_name, last_name=last_name, birth_date=birth_date,
                            password=generate_password_hash(password1, method='sha256'), creation_date=creation_date)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(created_account, category='succes')
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
                        flash(new_password_short, category='error')
                        pass
                    else:
                        # Update the user to the database
                        user_update = current_user
                        user_update.password = generate_password_hash(password1, method='sha256')
                        db.session.add(user_update)
                        db.session.commit()
                        login_user(user_update, remember=True)
                        flash(update_pass_succes, category='succes')
                        return redirect(url_for('auth.account'))
                else:
                    flash(same_password, category='error')

            else:
                flash(password_old_wrong, category='error')
    return render_template("account.html", user=current_user)
