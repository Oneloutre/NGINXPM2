import os

from flask import render_template, request, redirect, url_for
import bcrypt
import hashlib
import requests


def register_user():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if isformempty(request.form):
            error = 'Please fill all the fields'
            return render_template('auth/register/register.html', error=error)

        if password != confirm_password:
            error = 'Passwords do not match'
        else:
            crypted_username, crypted_email, crypted_password = crypt_data(username, email, password)
            get_gravatar_icon(email)
            with open('user_files/admin/admin.json', 'w') as file:
                file.write('{\n   "username": "' + crypted_username.decode('utf-8') + '",\n   "email": "' + crypted_email.decode('utf-8') + '",\n   "password": "' + crypted_password.decode('utf-8') + '"\n}')
            return redirect(url_for('login'))
    return render_template('auth/register/register.html', error=error)


def isformempty(form):
    for key in form:
        if form[key] == "":
            return True
    return False


def crypt_data(username, email, password):
    crypted_username = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt())
    crypted_email = bcrypt.hashpw(email.encode('utf-8'), bcrypt.gensalt())
    crypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return crypted_username, crypted_email, crypted_password


def get_gravatar_icon(email):
    os.mkdir('user_files')
    os.mkdir('user_files/admin')
    code = hashlib.md5(email.strip().encode('utf8')).hexdigest()
    mail_url = f"https://www.gravatar.com/avatar/{code}?size=2048"
    img_data = requests.get(mail_url)
    if img_data.status_code == 200:
        with open('user_files/admin/admin_avatar.png', 'wb') as f:
            f.write(img_data.content)

    else:
        img_data = requests.get("http://www.gravatar.com/avatar/?d=mp").content
        with open('user_files/admin/admin_avatar.png', 'wb') as f:
            f.write(img_data)
