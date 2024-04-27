import json
import os
import uuid


def first_instance(url, user, password, token):
    newid = str(uuid.uuid4())
    instance = {
        "instances": {
            newid: {
                "url": url,
                "credentials": {
                    "username": user,
                    "password": password,
                    "token": token
                }
            }
        }
    }
    return instance


def append_instance(url, user, password, token):
    instance = {
            "url": url,
            "credentials": {
                "username": user,
                "password": password,
                "token": token
            }
        }
    return instance


def register_instance(url, user, password, token):

    filepath = 'user_files/instances.json'

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            instance = first_instance(url, user, password, token)
            json.dump(instance, f, indent=4)
        return 'We are processing your instance...\n'
    else:
        with open(filepath, 'r+') as f:
            data = json.load(f)
            for instance_key, instance_data in data["instances"].items():
                if instance_data["url"] == url:
                    return 'An instance with the same URL already exists.\n'
                else:
                    instance_key = str(uuid.uuid4())
                    data["instances"][instance_key] = append_instance(url, user, password, token)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    return 'We are processing your instance...\n'
