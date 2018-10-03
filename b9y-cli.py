from sys import argv
import requests, json, signal, shlex

default_user = "admin"
default_password = "changeme"
default_host="http://localhost:8080"

def signal_handler(sig, frame):
        print('Bye!')
        exit(0)

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

def b9y_get_auth(h, u, p):
    url = h + "/auth/token?raw"
    payload = {'username': u, 'password': p}
    headers = {'Content-Type': "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        return(response.text)
    else:
        print "Unable to login with these connection details."
        exit(1)

def b9y_get(h, t, args):
    if len(args) != 1:
        print "ERROR: expecting exactly 1 argument, " + str(len(args)) + " given"
        exit

    url = h + "/keys/" + args[0]
    headers = {'Authorization': "Bearer:" + t}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        print "''" + response.text + "''"
    else:
        print "ERROR: key not found."

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    args = getopts(argv)

    if '-h' in args:
        b9y_host = args['-h']
    else:
        b9y_host = default_host

    if '-u' in args:
        b9y_user = args['-u']
    else:
        b9y_user = default_user

    if '-p' in args:
        b9y_password = args['-p']
    else:
        b9y_password = default_password

    token = b9y_get_auth(b9y_host, b9y_user, b9y_password)

    commands = ['get','set']

    while True:
        cmd_input = raw_input("> ")
        if cmd_input == "":
            continue
        # items = cmd_input.split()
        items = shlex.split(cmd_input, posix=False)
        cmd = items[0]
        cmd_args = items[1:99]

        if cmd not in commands:
            print "??"
        print "Command: " + cmd
        print "Args: " + str(cmd_args)
        exit
        if cmd == 'get':
            b9y_get(b9y_host, token, cmd_args)
