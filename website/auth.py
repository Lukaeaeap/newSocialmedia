# for the login, logout and sign up
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .__init__ import mail
import json
from flask_mail import Message
import random
import string
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

auth = Blueprint('auth', __name__)

LANGUAGE = "nl"

with open(f"website/static/languages/{LANGUAGE}.json", "r") as f:
    textlg = json.load(f)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Filter the user for the email, and look at the first email (which is unique so there is only one).
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(textlg['flashes']['logged_in'], category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(textlg['flashes']['wrong_password'], category='error')
        else:
            flash(textlg['flashes']['no_match'], category='error')
    return render_template("login.html", user=current_user)


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Filter the user for the email, and look at the first email (which is unique so there is only one).
        user = User.query.filter_by(email=email).first()
        if user and user.email == email:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            user.hashCode = hashCode
            db.session.commit()
            msg = Message(textlg['messages']['mail_subject'],
                          sender="luukspamlol@gmail.com",
                          recipients=[email])
            msg.body = f"{textlg['messages']['mail_greet']} {user.first_name},\n\n{textlg['messages']['mail_content']}\n\nhttp://localhost:5000/new-password/{user.hashCode}"
            mail.send(msg)
            print(email)
            flash(textlg['flashes']['email_sent'], category='succes')
        else:
            flash(textlg['flashes']['email_nonexistent'], category='error')
    return render_template("forgot_password.html", user=current_user)


@auth.route("/new-password/<string:hashCode>", methods=["GET", "POST"])
def new_password(hashCode):
    user = User.query.filter_by(hashCode=hashCode).first()
    print(user)
    if user:
        if request.method == 'POST':
            password1 = request.form['password_new1']
            password2 = request.form['password_new2']
            if password1 != password2:
                flash(textlg['flashes']['password_no_match'], category='error')
            elif len(password1) < 7:
                flash(textlg['flashes']['new_password_short'], category='error')
            else:
                user.password = generate_password_hash(password1, method='sha256')
                user.hashCode = None
                db.session.commit()
                login_user(user, remember=True)
                flash(textlg['flashes']['update_pass_succes'], category='succes')
                return redirect(url_for('views.home'))
        return render_template("new_password.html", user=user)
    else:
        flash(textlg['flashes']['token_expired'], category='error')
        return redirect(url_for('auth.login'))


# @auth.route('/new-password', methods=['GET', 'POST'])
# def new_password():
#     print(f"user: {current_user}")
#     if request.method == 'POST':
#         print("Somethings at least works..")
#     return render_template("new_password.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(textlg['flashes']['logged_out'], category='succes')
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
            flash(textlg['flashes']['email_exists'], category='error')
        elif user_check2:
            flash(textlg['flashes']['username_exists'], category='error')
        elif len(email) < 4:
            flash(textlg['flashes']['email_short'], category='error')
        elif len(first_name) < 2:
            flash(textlg['flashes']['firstname_short'], category='error')
        elif password1 != password2:
            flash(textlg['flashes']['password_no_match'], category='error')
        elif len(password1) < 7:
            flash(textlg['flashes']['password_short'], category='error')
        else:
            # Add the user to the database
            new_user = User(email=email, first_name=first_name, user_name=user_name, last_name=last_name, birth_date=birth_date,
                            password=generate_password_hash(password1, method='sha256'), creation_date=creation_date)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(textlg['flashes']['created_account'], category='succes')
            # when logged in go back to the home page
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


@ login_required
@auth.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        if 'submit-password' in request.form:
            print("Changing password")
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
                            flash(textlg['flashes']['new_password_short'], category='error')
                            pass
                        else:
                            # Update the user to the database
                            user_update = current_user
                            user_update.password = generate_password_hash(password1, method='sha256')
                            db.session.add(user_update)
                            db.session.commit()
                            login_user(user_update, remember=True)
                            flash(textlg['flashes']['update_pass_succes'], category='succes')
                            return redirect(url_for('auth.account'))
                    else:
                        flash(textlg['flashes']['same_password'], category='error')
                else:
                    flash(textlg['flashes']['old_password_wrong'], category='error')
        elif 'submit-settings' in request.form:
            username_new = request.form.get('userNameNew')
            email_new = request.form.get('emailNew')

            user_mail_check = User.query.filter_by(email=email_new).first()
            user_name_check = User.query.filter_by(user_name=username_new).first()
            if user_mail_check and user_mail_check.email != current_user.email:
                flash(textlg['flashes']['email_exists'], category='error')
            elif user_name_check and user_name_check.user_name != current_user.user_name:
                flash(textlg['flashes']['username_exists'], category='error')
            elif len(email_new) < 4:
                flash(textlg['flashes']['email_short'], category='error')
            elif email_new != current_user.email or username_new != current_user.user_name:
                # Update the user to the database
                user_update = current_user
                user_update.email = email_new
                user_update.user_name = username_new
                db.session.add(user_update)
                db.session.commit()
                login_user(user_update, remember=True)
                flash(textlg['flashes']['update_account_succes'], category='succes')
                return redirect(url_for('auth.account'))
        elif 'submit-profile' in request.form:
            first_name_new = request.form.get('firstNameNew')
            last_name_new = request.form.get('lastNameNew')
            birth_date_new = request.form.get('birthDateNew')
            if first_name_new != current_user.first_name or last_name_new != current_user.last_name or birth_date_new != current_user.birth_date:
                user_update = current_user
                user_update.first_name = first_name_new
                user_update.last_name = last_name_new
                user_update.birth_date = birth_date_new
                db.session.add(user_update)
                db.session.commit()
                login_user(user_update, remember=True)
                flash(textlg['flashes']['update_account_succes'], category='succes')
                return redirect(url_for('auth.account'))
    return render_template("account.html", user=current_user)
