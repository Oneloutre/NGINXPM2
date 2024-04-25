import cloudscraper
from flask import render_template, request, redirect, url_for, make_response, jsonify, session

scraper = cloudscraper.create_scraper()

def proxy_add_new(csrf_access_token):
    error = None
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
                    if response == "Host seems up and running !":
                        return render_template('misc/add_proxy.html', success='Host seems up and running.')
                    elif response == "Timeout Error":
                        error = 'Timeout Error'
                    else:
                        error = 'Error fetching the URL'
                except:
                    error = ''
    return render_template('misc/add_proxy.html', error=error)

def validate(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    else:
        return True


#def check_proxy_validity(url, timeout=5):


def timeout_checker(url, timeout=5):
    try:
        response = scraper.get(url, timeout=timeout)
        response.raise_for_status()
        return 'Host seems up and running !'
    except Exception as e:
        print(e)
        if "Read timed out" in str(e):
            return 'Timeout Error'
        else:
            return 'Error'
