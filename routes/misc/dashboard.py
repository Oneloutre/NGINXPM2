import os
import json
import cloudscraper
import favicon
scraper = cloudscraper.create_scraper()


def analyze_instances(instances_file):
    list_of_urls = []
    if not os.path.exists('user_files/instances'):
        os.mkdir('user_files/instances')
    if os.path.exists(instances_file):
        with open(instances_file, 'r') as f:
            instances = json.load(f)
        for instance_id, instance_info in instances["instances"].items():
            url = url_without_prefix(instance_info["url"])
            list_of_urls.append(url)
            if not os.path.exists(f'user_files/instances/{url}'):
                os.mkdir(f'user_files/instances/{url}')
        return list_of_urls
    else:
        return []


def scrap_instance(url):
    url_backend = url_without_prefix(url)
    with open('user_files/instances.json', 'r') as f:
        instances = json.load(f)
    for instance_id, instance_info in instances["instances"].items():
        token = instance_info["credentials"]["token"]

        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }
        hosts = scraper.get(url+'/api/nginx/proxy-hosts', headers=headers)
        dumped = json.dumps(hosts.json(), indent=4)
        if not os.path.exists(f'user_files/instances/{url_backend}'):
            os.mkdir(f'user_files/instances/{url_backend}')
        with open(f'user_files/instances/{url_backend}/hosts.json', 'w') as f:
            f.write(dumped)


def display_instance(url):
    domain_names = []
    if os.path.exists('user_files/instances'):
        with open(f'user_files/instances/{url}/hosts.json', 'r') as f:
            hosts = json.load(f)
            for host in hosts:
                domain_names.append(host["domain_names"])
        return domain_names


def get_favicons(urls):
    favicons = []
    for url in urls:
        try:
            url_icon = "https://"+str(url[0])
            icons = favicon.get(url_icon)[0]
            favicons.append(icons)
            print(icons)
        except Exception as e:
            favicons.append("https://comptoir-du-libre.org/img/files/Softwares/Nginx%20Proxy%20Manager/avatar/icon.png")
            print(e)
    return favicons



def url_without_prefix(url):
    if "https://" in url:
        url = url.replace("https://", "")
    elif "http://" in url:
        url = url.replace("http://", "")
    return url