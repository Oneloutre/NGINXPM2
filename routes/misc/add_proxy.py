import cloudscraper
from flask import render_template, request, jsonify
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

def proxy_add_new(csrf_access_token):
    error = None
    if request.method == 'POST':
        return check_nginx_validity(csrf_access_token)
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
        if csrf_access_token != request.form['csrf_token']:
            return jsonify({'error': 'Invalid CSRF token'}), 400
        else:
            url_form = request.form['target']
            url = url_form.strip()
            if not url:
                error = 'URL is required.'
                return render_template('misc/add_proxy.html', error=error)
            else:
                if validate(url):
                    pass
                else:
                    url = 'http://' + url
                try:
                    response = timeout_checker(url)
                    if response == 'host_up':
                        return render_template('misc/add_proxy.html', success='Host is up and running !')
                    elif response == "Timeout Error":
                        error = 'Timeout Error'
                        return render_template('misc/add_proxy.html', error=error)
                    elif response == 'not_nginx_proxy_manager':
                        error = 'Error... This is not a Nginx Proxy Manager URL !'
                        return render_template('misc/add_proxy.html', error=error)
                    else:
                        error = 'Error fetching the URL'
                        return render_template('misc/add_proxy.html', error=error)
                except:
                    return render_template('misc/add_proxy.html', error='Error fetching the URL')
                    error = ''


def authenticate_user_in_nginx(user, password):
    pass