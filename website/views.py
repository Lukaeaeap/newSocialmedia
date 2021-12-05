# The file where we write how the user navigates trough the site
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

LANGUAGE = "nl"

with open(f"website/static/languages/{LANGUAGE}.json", "r") as f:
    textlg = json.load(f)
# flash(textlg['flashes']['no_match'], category='error')


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # The home page for www.website.com/ the slash means it is the home page since we called it that.
    if request.method == 'POST':
        note = request.form.get('note')
        note_text_check = Note.query.filter_by(data=note).first()
        # note_text_check = Note.query.filter_by(data=note).first()
        print(note_text_check)
        boolean_pass = True

        if note_text_check:
            note_user_check = Note.query.filter(note_text_check.user_id == current_user.id).first()
            print(note_user_check)
            if note_user_check:
                flash(textlg['flashes']['already_added'], category='error')
                boolean_pass = False
            else:
                boolean_pass = True
        if len(note) < 1:
            flash(textlg['flashes']['post_short'], category='error')
        elif boolean_pass:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash(textlg['flashes']['post_succes'], category='succes')

    Notes = Note.query.all()
    Users = User.query.all()
    # for user in Users:
    #     print(user.user_name)

    return render_template("home.html", user=current_user, posts=Notes, people=Users)


@ views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
