import cloudscraper
from flask import render_template, request, jsonify, redirect, url_for
from bs4 import BeautifulSoup
import json
from routes.misc.instances_management import register_instance

scraper = cloudscraper.create_scraper()


def proxy_add_new(csrf_access_token):
    error = None
    if request.method == 'POST':
        if not 'username' in request.form:
            return check_nginx_validity(csrf_access_token)
        else:
            return authenticate_user_in_nginx(request.form['target'], request.form['username'], request.form['password'], csrf_access_token, request.form['csrf_token'])
        return render_template('misc/add_proxy.html', error=error)
    elif request.method == 'GET':
        return render_template('misc/add_proxy.html', error=error)


def validate(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    else:
        return True


def timeout_checker(url, timeout=5):
    try:
        response = scraper.get(url, timeout=timeout)
        response.raise_for_status()
        title = BeautifulSoup(response.text, 'html.parser').title.string
        if title == 'Nginx Proxy Manager':
            return 'host_up'
        else:
            return 'not_nginx_proxy_manager'
    except Exception as e:
        if "Read timed out" in str(e):
            return 'Timeout Error'
        else:
            return 'Error'


def check_nginx_validity(csrf_access_token):
    if request.method == 'POST':
        csrf_token = request.form['csrf_token']

        if csrf_access_token != csrf_token:
            return jsonify({'error': 'Invalid CSRF token'}), 400
        else:
            url_form = request.form['target']
            url = url_form.strip()
            if not url:
                error = 'URL is required.'
                return render_template('misc/add_proxy.html', target_error=error)
            else:
                if validate(url):
                    pass
                else:
                    url = 'http://' + url
                try:
                    response = timeout_checker(url)
                    if response == 'host_up':
                        return render_template('misc/add_proxy.html', target_success='Host is up and running !')
                    elif response == "Timeout Error":
                        error = 'Timeout Error'
                        return render_template('misc/add_proxy.html', target_error=error)
                    elif response == 'not_nginx_proxy_manager':
                        error = 'This is not a Nginx Proxy Manager URL !'
                        return render_template('misc/add_proxy.html', target_error=error)
                    else:
                        error = 'Error fetching the URL'
                        return render_template('misc/add_proxy.html', target_error=error)
                except:
                    return render_template('misc/add_proxy.html', target_error='Error fetching the URL')


def authenticate_user_in_nginx(url, user, password, csrf_access_token, csrf_sent_token):
    csrf_access_token = csrf_access_token
    csrf_sent_token = csrf_sent_token
    if csrf_access_token != csrf_sent_token:
        return jsonify({'error': 'Invalid CSRF token'}), 400
    if not verify_credentials_validity(url, user, password):
        return render_template('misc/add_proxy.html', error='Please fill all the fields')
    else:

        nginx_url = url+'/api/tokens'
        nginx_user = user
        nginx_password = password

        try:
            form = {
                'identity': nginx_user,
                'secret': nginx_password
            }
            response = scraper.post(nginx_url, data=form)
            jsonified = response.json()
            if 'error' in jsonified:
                return render_template('misc/add_proxy.html', error=jsonified['error']['message'])
            else:
                token = jsonified['token']
                headers = {
                    'Authorization': f'Bearer {token}',
                    'accept': 'application/json'
                }
                try:
                    hosts = scraper.get(url+'/api/nginx/proxy-hosts', headers=headers)
                    get_hosts(hosts)
                    message = register_instance(url, nginx_user, nginx_password, token)
                    return render_template('misc/please_wait.html', message=message)
                except Exception as e:
                    return render_template('misc/add_proxy.html', error='Error fetching the hosts')
                return redirect(url_for('please_wait'))
        except Exception as e:
            print(e)


def verify_credentials_validity(url, user, password):
    if not url or not user or not password:
        return False
    else:
        return True


def get_hosts(hosts):
    json_dumped = json.dumps(hosts.json(), indent=4)
    with open('user_files/hosts.json', 'w') as file:
        file.write(json_dumped)
