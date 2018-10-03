from sys import argv
import requests, json

default_user = "admin"
default_password = "changeme"
default_host="http://localhost:8080"

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

def b9y_get_auth():
    url = "http://localhost:8080/auth/token"
    payload = '{"username": "admin", "password": "changeme"}'
    headers = {'Content-Type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)


if __name__ == '__main__':
    myargs = getopts(argv)
    if '-i' in myargs:  # Example usage.
        print(myargs['-i'])
    print(myargs)

    b9y_get_auth()
cmd = raw_input("> ")

print cmd
