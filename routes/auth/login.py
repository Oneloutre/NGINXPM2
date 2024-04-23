from flask import render_template, request, redirect, url_for, make_response
import json, bcrypt

def log_in():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        encrypted_username, encrypted_email, encrypted_password = load_encrypted_creds('user_files/admin/admin.json')

        if bcrypt.checkpw(username.encode('utf8'), encrypted_username) or bcrypt.checkpw(username.encode('utf8'), encrypted_email) and bcrypt.checkpw(password.encode('utf8'), encrypted_password):
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login/login.html', error=error)
    return render_template('login/login.html', error=error)


def load_encrypted_creds(file):
    loaded_json = json.load(open(file))
    username = loaded_json["username"].encode('utf8')
    email = loaded_json["email"].encode('utf8')
    password = loaded_json["password"].encode('utf8')
    return username, email, password



