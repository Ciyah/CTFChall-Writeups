from pathlib import Path
import uuid
import secrets
import os
import hashlib
import markdown
from flask import Flask, jsonify, request, redirect, url_for
import chameleon_flask
from sqlalchemy import text
from models import db, User, ChatMessage, Announcement
from auth import setup_auth, generate_token, verify_token
from datetime import datetime
from chameleon import PageTemplate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

dev_mode = False
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = str(BASE_DIR) + "/uploads"
template_folder = str(BASE_DIR / "templates")
chameleon_flask.global_init(template_folder, auto_reload=dev_mode)

# Make the uploads folder
if not os.path.exists(UPLOADS_DIR):
    os.mkdir(UPLOADS_DIR)
else:
    print("uploads exists")

print(UPLOADS_DIR)

db.init_app(app)
kid, *keys = setup_auth()

admin_username = f"bobby_{secrets.token_hex(10)}"
admin_plaintext_password = secrets.token_hex(32)
admin_password = hashlib.sha256(f"{admin_plaintext_password}".encode()).hexdigest()
admin_token = secrets.token_hex(16)

with open("/shared/.env", mode="w") as file:
    file.write(
        f"ADMIN_USERNAME={admin_username}\nADMIN_PASSWORD={admin_plaintext_password}"
    )

print(
    f"Admin Credentials:- {admin_username}:{admin_plaintext_password}\nAdmin Token: {admin_token}"
)

with app.app_context() as cxt:
    db.create_all()
    admin_user = User(
        username=admin_username,
        password=admin_password,
        id=str(uuid.uuid4()),
        token=admin_token,
        role="admin",
    )
    db.session.add(admin_user)
    db.session.commit()


@app.route("/")
@chameleon_flask.template("index.pt")
def home():
    return {"message": "Hi"}


@app.route("/register", methods=["GET", "POST"])
@chameleon_flask.template("register.pt")
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
            user_id = str(uuid.uuid4())
            new_user = User(
                id=user_id,
                username=username,
                password=password,
                role="chatter",
                token=str(hashlib.md5(username.encode()).hexdigest()),
            )
            db.session.add(new_user)
            db.session.commit()
            response = redirect(url_for("login"))
            return response
        except Exception as e:
            print(e)
            return {"message": "Something Went Wrong"}
    if request.method == "GET":
        return {"message": ""}


@app.route("/login", methods=["GET", "POST"])
@chameleon_flask.template("login.pt")
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        try:
            db_entry = User.query.filter_by(username=username).first()
            if db_entry and db_entry.password == password:
                token = generate_token({"user_id": db_entry.id}, kid)
                response = redirect(url_for("chat_home"))
                response.set_cookie("auth_token", token)
                return response
            else:
                return {"message": "Wrong Credentials"}
        except Exception as e:
            print(e)
            return {"message": "Something went wrong"}
    return {"message": ""}


@app.route("/profile", methods=["GET", "POST"])
@chameleon_flask.template("profile.pt")
def profile():
    if request.method == "GET":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return redirect(url_for("login"))
        decoded = verify_token(cookie)
        if not decoded:
            return redirect(url_for("login"))
        uid = decoded["user_id"]
        user = User.query.filter_by(id=uid).first()
        if not user:
            return redirect(url_for("register"))
        return {"user_data": [], "token": user.token}
    if request.method == "POST":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return redirect(url_for("login"))
        decoded = verify_token(cookie)
        if not decoded:
            return redirect(url_for("login"))
        uid = decoded["user_id"]
        user = User.query.filter_by(id=uid).first()
        if not user:
            return redirect(url_for("register"))
        token = request.form.get("token")
        user_data = (
            db.session.query(User).filter(text("token='{}'".format(token))).all()
        )
        print(user_data)
        return {"user_data": user_data, "token": user.token}


@app.route("/logout")
def logout():
    response = redirect(url_for("login"))
    response.set_cookie("auth_token", "")
    return response


@app.route("/api/chat-messages", methods=["GET", "POST"])
def chat_messages():
    # Return username, nickname, message, timestamp
    if request.method == "POST":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return jsonify({"error": "unauthorized"}), 401
        dictionary = verify_token(cookie)
        if not dictionary:
            return jsonify({"error": "unauthorized"}), 401
        else:
            username = User.query.filter_by(id=dictionary["user_id"]).first().username
            message = request.form.get("message")
            file = request.files.get("attachment")
            new_chat_message = ChatMessage(
                timestamp=str(datetime.now()),
                content=message,
                sender=username,
                attachments=UPLOADS_DIR + "/" + file.filename,
            )
            if file.filename:
                file.save(UPLOADS_DIR + "/" + file.filename)
            db.session.add(new_chat_message)
            db.session.commit()
            return redirect(url_for("chat_home"))
    if request.method == "GET":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return jsonify({"error": "unauthorized"}), 401
        dictionary = verify_token(cookie)
        if not dictionary:
            return jsonify({"error": "unauthorized"}), 401
        messages = ChatMessage.query.all()
        json_array = []
        for i in messages:
            json_array.append([i.timestamp, i.content, i.sender, i.attachments])
        return jsonify({"success": True, "messages": json_array})
    return {}


@app.route("/api/announcements", methods=["GET", "POST"])
def announcements():
    if request.method == "GET":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return jsonify({"error": "unauthorized"}), 401
        dictionary = verify_token(cookie)
        if not dictionary:
            return jsonify({"error": "unauthorized"}), 401
        user_id = dictionary["user_id"]
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "unauthorized"}), 401
        announcements_array = Announcement.query.filter_by(
            receiver=user.username
        ).first()
        if user.username == admin_username:
            announcements_array = Announcement.query.filter_by(sender=user.username)
        json_array = []
        if announcements_array:
            for i in announcements_array:
                json_array.append([i.id, i.timestamp, i.sender, i.receiver])
        return jsonify(json_array), 200

    if request.method == "POST":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return jsonify({"error": "unauthorized"}), 401
        dictionary = verify_token(cookie)
        if not dictionary:
            return jsonify({"error": "unauthorized"}), 401
        user_id = dictionary["user_id"]
        user = User.query.filter_by(id=user_id).first()
        if not user or user.username != admin_username:
            return jsonify({"error": "unauthorized"}), 401

        title = request.form.get("title")
        content = markdown.markdown(request.form.get("announcement"))
        if content:
            for i in '$#{}"_.':
                content = content.replace(i, "")
        tpl = PageTemplate(content)
        res = tpl.render()
        users = User.query.all()
        for i in users:
            new_announcement = Announcement(
                timestamp=str(datetime.now()),
                sender=user.username,
                content=res,
                title=title,
                receiver=i.username,
            )
            db.session.add(new_announcement)
        db.session.commit()
        return jsonify({"success": True}), 200


@app.route("/chat", methods=["GET"])
@chameleon_flask.template("chat/index.pt")
def chat_home():
    cookie = request.cookies.get("auth_token", "")
    if not cookie:
        return redirect(url_for("login"))
    dictionary = verify_token(cookie)
    if not dictionary:
        return redirect(url_for("login"))
    user = User.query.filter_by(id=dictionary["user_id"]).first()
    if user:
        token = user.token
    else:
        token = ""
    return {"token": token}


@app.route("/announcements", methods=["GET", "POST"])
@chameleon_flask.template("announcements/index.pt")
def announcements_home():
    if request.method == "GET":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return redirect(url_for("login"))
        decoded = verify_token(cookie)
        if not decoded:
            return redirect(url_for("login"))
        uid = decoded["user_id"]
        user = User.query.filter_by(id=uid).first()
        if not user:
            return redirect(url_for("register"))
        announcements = Announcement.query.all()
        return {"announcements": announcements}
    if request.method == "POST":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return redirect(url_for("login"))
        decoded = verify_token(cookie)
        if not decoded:
            return redirect(url_for("login"))
        uid = decoded["user_id"]
        user = User.query.filter_by(id=uid).first()
        if not user:
            return redirect(url_for("register"))

        return {"token": user.token}


@app.route("/announcements/view", methods=["GET"])
@chameleon_flask.template("announcements/view.pt")
def announcements_view():
    cookie = request.cookies.get("auth_token", "")
    if not cookie:
        return redirect(url_for("login"))
    decoded = verify_token(cookie)
    if not decoded:
        return redirect(url_for("login"))
    uid = decoded["user_id"]
    user = User.query.filter_by(id=uid).first()
    if not user:
        return redirect(url_for("register"))
    return {"token": user.token}


@app.route("/admin/announcements", methods=["GET", "POST"])
@chameleon_flask.template("admin/index.pt")
def admin_home():
    if request.method == "GET":
        cookie = request.cookies.get("auth_token", "")
        if not cookie:
            return redirect(url_for("login"))
        decoded = verify_token(cookie)
        if not decoded:
            return redirect(url_for("login"))
        user_id = decoded["user_id"]
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return redirect(url_for("register"))
        if user and user.username != admin_username:
            return redirect(url_for("chat_home"))
        return {"token": user.token}


if __name__ == "__main__":
    app.run(debug=dev_mode, host="0.0.0.0", port=3000)

