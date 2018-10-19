#!/usr/bin/env python
import requests, json, re

default_user = "admin"
default_password = "changeme"
default_host="http://localhost:8080"

class B9y:

    def __init__(self, endpoint = default_host, username = default_user, password = default_password):
        self.endpoint = endpoint
        self.username = username
        self.password = password

        url = self.endpoint + "/auth/token?raw"
        payload = {'username': self.username, 'password': self.password}
        headers = {'Content-Type': "application/json"}

        try:
            response = requests.request("POST", url, json=payload, headers=headers)
        except:
            raise ValueError("ERROR: Cannot connect to " + self.endpoint)
            exit(1)
        if response.status_code == 200:
            self.token = response.text
            return(None)
        else:
            raise ValueError("ERROR: Unable to login with these connection details.")
            exit(1)

    def get_token(self):
        return(self.token)
    def info(self):
        url = self.endpoint + "/"
        response = requests.request("GET", url)
        if response.status_code == 200:
            res = json.loads(response.text)
            return res["instance"], res["release"]

    def save(self):
        url = self.endpoint + "/save"
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def get(self, key):
        url = self.endpoint + "/keys/" + str(key)
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def uget(self, key, userid):
        url = self.endpoint + "/keys/" + str(key) + "?userid=" + str(userid)
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def keys(self, search=""):
        url = self.endpoint + "/keys"
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            res = json.loads(response.text)
            rkeys=[]
            for k in res['keys']:
                found_key = k['key']
                found_owner = k['owner']
                if re.search(search, found_key):
                    if self.username == 'admin' and found_owner != "0":
                        rkeys.append(found_key + " (OWNER:" + found_owner + ")")
                    else:
                        rkeys.append(found_key)
            return(rkeys)
        else:
            return(None)

    def incr(self, key):
        url = self.endpoint + "/incr/" + str(key)
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def set(self, key, value):
        url = self.endpoint + "/keys/" + key
        headers = {'Authorization': "Bearer:" + self.token}
        payload = value
        response = requests.request("PUT", url, data=payload, headers=headers)

        if response.status_code == 200:
            return(True)
        else:
            raise ValueError("ERROR: key invalid or quota exceeded (" + str(response.status_code) + ")")

    def push(self, key, value):
        url = self.endpoint + "/lists/" + key
        headers = {'Authorization': "Bearer:" + self.token}
        payload = value
        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code == 200:
            return(True)
        else:
            raise ValueError("ERROR: key invalid or quota exceeded (" + str(response.status_code) + ")")

    def pop(self, key):
        url = self.endpoint + "/lists/" + key
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def create_user(self, username, password):
        url = self.endpoint + "/users"
        headers = {'Authorization': "Bearer:" + self.token, 'Content-Type':'application/json'}
        payload = {}
        payload["email"] = username
        payload["password"] = password
        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200:
            j = json.loads(response.text)
            return(j["id"])
        else:
            raise ValueError("ERROR (" + str(response.status_code) + ")")

    def list_users(self):
        url = self.endpoint + "/users"
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(json.loads(response.text))
        else:
            return(None)


    def create_route(self, key, content_type):
        url = self.endpoint + "/routes"
        headers = {'Authorization': "Bearer:" + self.token, 'Content-Type':'application/json'}
        payload = {}
        payload["key"] = key
        payload["content_type"] = content_type
        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200:
            j = json.loads(response.text)
            return(j["path"])
        else:
            raise ValueError("ERROR (" + str(response.status_code) + ")")

    def set_admin_password(self, new_pass):
        url = self.endpoint + "/config/admin"
        headers = {'Authorization': "Bearer:" + self.token, 'Content-Type':'application/json'}
        payload = {}
        payload["password"] = new_pass
        response = requests.request("PUT", url, json=payload, headers=headers)

        if response.status_code == 200:
            return(True)
        else:
            raise ValueError("ERROR (" + str(response.status_code) + ")")
