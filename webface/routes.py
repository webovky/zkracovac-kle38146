from . import app
from flask import render_template, request, redirect, url_for, session, flash
import functools
from werkzueg.security import check_password_hash, generate_password_hash 
from .models import User
from pony.orm import db_session
# from werkzeug.security import check_password_hash

slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
@db_session
def index():
    temp = []
    for user in User.select():
        temp.append ((user.nick, user.passwd))       
    return render_template("base.html.j2")


@app.route("/add/", methods=["GET"])
def add():
    return render_template("add.html.j2")

@app.route("/add/", methods=["POST"])
@db_session
def add_post():
    nick = request.form.get("nick")
    passwd1 = request.form.get("passwd1")
    passwd2 = request.form.get("passwd2")

    if not all([nick,passwd1,passwd2]):
        flash("Musíš vše vyplnit")

    else:
        user = User.get (nick=nick)
        if user:
            flash("Tento uživatel již existuje!")
        elif passwd1 != passwd2:
            flash("Hesla nejsou stejná!")

        else:

            user = User(nick=nick, passwd=generate_password_hash(passwd1))
            flash("Uživatel vytvořen")




    return redirect(url_for("add"))    


@app.route("/abc/", methods=["POST"])
def abc():
    return render_template("abc.html.j2", slova=slova)



@app.route("/login/", methods=["POST"])
@db_session
def login_post():
    return render_template("login.html.j2")
    
"""


<h1>Text</h1>

<p>toto je text</p>

"""
