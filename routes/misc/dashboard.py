import os
import json
import cloudscraper

scraper = cloudscraper.create_scraper()


def analyze_instances(instances_file):
    list_of_urls = []
    if not os.path.exists('user_files/instances'):
        os.mkdir('user_files/instances')
    if os.path.exists(instances_file):
        with open(instances_file, 'r') as f:
            instances = json.load(f)
        for instance_id, instance_info in instances["instances"].items():
            url = instance_info["url"]
            list_of_urls.append(url)
            if not os.path.exists(f'user_files/instances/{instance_id}'):
                os.mkdir(f'user_files/instances/{instance_id}')
        return list_of_urls
    else:
        return []


def scrap_instance(url):
    with open('user_files/instances.json', 'r') as f:
        instances = json.load(f)
    for instance_id, instance_info in instances["instances"].items():
        id = instance_id
        token = instance_info["credentials"]["token"]

        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }
        hosts = scraper.get(url+'/api/nginx/proxy-hosts', headers=headers)
        print(hosts.json())
        dumped = json.dumps(hosts.json(), indent=4)
        if not os.path.exists(f'user_files/instances/{id}'):
            os.mkdir(f'user_files/instances/{id}')
        with open(f'user_files/instances/{id}/hosts.json', 'w') as f:
            f.write(dumped)

