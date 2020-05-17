from flask import Flask, url_for, render_template, redirect, request, session
from app import app
from app import db
from models import Users, Photos, Friends, Messages, Requests
import os


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    if session.get("user"):
        return redirect("/home")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        us = Users.query.filter_by(login=username, password=password).all()
        session['user'] = us[0].user_id
        return redirect('/home')
    return render_template('login.html')


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST" and request.form["password_1"] == request.form["password_2"]:
        username = request.form["login"]
        password = request.form["password_1"]
        us = Users.query.filter_by(login=username, password=password).all()

        if len(us) == 0:
            user = Users(request.form["firstname"],
                         request.form["lastname"],
                         request.form["login"],
                         request.form["password_1"],
                         request.form["email"],
                         request.form["gender"])
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        return 'Incorrect login or password'
    return redirect("/")


@app.route("/home")
def home():
    user = session['user']
    us = Users.query.get(user)
    return render_template("HomePage.html", user=us)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        se = request.form['search'].split()
        sea = Users.query.filter(Users.firstname.startswith(se[0])).all()  # firstname=se
        if len(se) > 1:
            sea.extend(Users.query.filter(Users.lastname.startswith(se[1])).all())
        setlist = []
        for i in sea:
            if i not in setlist:
                setlist.append(i)
        return render_template('Search.html', list=setlist)
    return 'Error'


@app.route("/requests")
@app.route("/requests/<receiver>", methods=["POST", "GET"])
def requests(receiver=None):
    if request.method == "POST":
        receiver = int(receiver)
        req = Requests(session["user"], receiver)
        db.session.add(req)
        db.session.commit()
        return redirect("/page/" + str(receiver))
    reqs = Requests.query.filter_by(user_2=session["user"]).all()
    senders = []
    for i in reqs:
        one = Users.query.get(i.user_1)
        senders.append(one)
    return render_template("requests.html", reqlist=senders)


@app.route("/acceptfriend/<sender>", methods=["GET", "POST"])
def accept(sender):
    if request.method == "POST":
        fr = Friends(sender, session["user"])
        db.session.add(fr)
        req = Requests.query.filter_by(user_1=int(sender)).all()
        for i in req:
            db.session.delete(i)
        db.session.commit()
    return redirect("/requests")


@app.route("/cancelfriend/<sender>", methods=["GET", "POST"])
def cancel(sender):
    if request.method == "POST":
        req = Requests.query.filter_by(user_1=int(sender)).all()
        for i in req:
            db.session.delete(i)
        db.session.commit()
    return redirect("/requests")


@app.route("/messages")
@app.route("/messages/<user>")
def messages(user=None):
    fl1 = Friends.query.filter_by(user_1=session['user']).all()
    fl2 = Friends.query.filter_by(user_2=session['user']).all()
    fl = []
    for i in fl1:
        us = Users.query.get(i.user_2)
        fl.append(us)
    for i in fl2:
        us = Users.query.get(i.user_1)
        fl.append(us)
    if user != None:
        us = Users.query.get(int(user))
        mes = Messages.query.filter_by(user_1=session['user'], user_2=int(user)).all()
        mes.extend(Messages.query.filter_by(user_2=session['user'], user_1=int(user)).all())
        mes.sort(key=lambda i: i.message_id)
        return render_template("Messages.html", flist=fl, us=us, mes=mes)
    return render_template("Messages.html", flist=fl, us=None, mes=[])


@app.route("/sendmessage/<user>", methods=["POST"])
def send(user):
    message = request.form["message"]
    mes = Messages(session["user"], int(user), message)
    db.session.add(mes)
    db.session.commit()
    return redirect("/message/" + user)


@app.route("/info")
def info():
    return render_template("Info.html")


@app.route("/photos")
def photos():
    ph = Photos.query.filter_by(user_id=session["user"]).all()
    ph.sort(key=lambda i: i.photos_id)
    return render_template("Photos.html", image=ph)


@app.route("/add_photo", methods=["POST", "GET"])
def add_photo():
    if request.method == "POST":
        p = request.files.get("photo")
        if p.filename != '':
            p.save(p.filename)
            x = open(p.filename, 'rb').read()
            y = open('static/images/' + p.filename, 'wb')
            y.write(x)
            os.remove(p.filename)
            ph = Photos(session["user"], p.filename)
            db.session.add(ph)
            db.session.commit()
    return redirect("/photos")


@app.route("/likephotos/<photo>")
def likephotos(photo):
    ph = Photos.query.get(int(photo))
    ph.like += 1
    db.session.commit()
    return redirect("/friendphoto/" + str(ph.user_id))


@app.route("/delphotos/<photo>")
def delphotos(photo):
    ph = Photos.query.get(int(photo))
    db.session.delete(ph)
    db.session.commit()
    return redirect("/photos")


@app.route("/friendphoto/<user>")
def friendphoto(user):
    ph = Photos.query.filter_by(user_id=int(user)).all()
    ph.sort(key=lambda i: i.photos_id)
    return render_template("friendphoto.html", image=ph)


@app.route("/friendfriend/<user>")
def friendfriend(user):
    flist = Friends.query.filter_by(user_1=int(user)).all()
    slist = Friends.query.filter_by(user_2=int(user)).all()
    friendlist = []
    for i in flist:
        one = Users.query.get(i.user_2)
        friendlist.append(one)
    for i in slist:
        one = Users.query.get(i.user_1)
        friendlist.append(one)
    return render_template("friendfriend.html", list=friendlist)


@app.route("/friends")
def friends():
    flist = Friends.query.filter_by(user_1=session["user"]).all()
    slist = Friends.query.filter_by(user_2=session["user"]).all()
    friendlist = []
    for i in flist:
        one = Users.query.get(i.user_2)
        friendlist.append(one)
    for i in slist:
        one = Users.query.get(i.user_1)
        friendlist.append(one)
    return render_template("Friends.html", list=friendlist)


@app.route("/deletefriend/<user>", methods=["POST", "GET"])
def deletefriend(user):
    us = Friends.query.filter_by(user_1=session["user"], user_2=int(user)).all()
    for i in us:
        db.session.delete(i)
    us = Friends.query.filter_by(user_2=session["user"], user_1=int(user)).all()
    for i in us:
        db.session.delete(i)
    db.session.commit()
    return redirect("/friends")


@app.route("/settings")
def settings():
    return render_template("Settings.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("login.html")


@app.route("/page/<id>")
def page(id):
    user = Users.query.get(int(id))
    return render_template("friendpage.html", user=user)


@app.route("/changepassword", methods=["POST"])
def chpass():
    user = Users.query.get(session["user"])
    if request.form.get("new") == request.form.get("new2") and request.form.get("old") == user.password:
        user.password = request.form.get("new")
        db.session.commit()
        return redirect("/settings")


@app.route("/changename", methods=["POST"])
def chnm():
    user = Users.query.get(session["user"])
    user.firstname = request.form.get("name")
    db.session.commit()
    return redirect("/settings")


@app.route("/changeemail", methods=["POST"])
def chem():
    user = Users.query.get(session["user"])
    user.email = request.form.get("email")
    db.session.commit()
    return redirect("/settings")


@app.route("/changebirthday", methods=["POST"])
def chbr():
    user = Users.query.get(session["user"])
    user.birthday = request.form.get("birthday")
    db.session.commit()
    return redirect("/settings")


if __name__ == '__main__':
    app.run(debug=True)
