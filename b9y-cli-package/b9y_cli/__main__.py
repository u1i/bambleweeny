#!/usr/bin/env python
from sys import argv
import requests, json, signal, shlex

b9y_cli_release = "0.01"
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

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
    except:
        print "ERROR: Cannot connect to " + h
        exit(1)
    if response.status_code == 200:
        return(response.text)
    else:
        print "ERROR: Unable to login with these connection details."
        exit(1)

def b9y_get_info(h, t):
    url = h + "/"
    response = requests.request("GET", url)
    if response.status_code == 200:
        res = json.loads(response.text)
        return res["instance"], res["release"]

def b9y_get(h, t, args):
    if len(args) != 1:
        print "ERROR: expecting exactly 1 argument, " + str(len(args)) + " given"
        return

    url = h + "/keys/" + args[0]
    headers = {'Authorization': "Bearer:" + t}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        print '"' + response.text + '"'
    else:
        print "ERROR: key not found."

def b9y_set(h, t, args):
    if len(args) != 2:
        print "ERROR: expecting exactly 2 argument, " + str(len(args)) + " given"
        return

    url = h + "/keys/" + args[0]
    headers = {'Authorization': "Bearer:" + t}
    payload = args[1]
    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code == 200:
        print "OK"
    else:
        print "ERROR: key not found."

def main():

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
    b9y_instance, b9y_release = b9y_get_info(b9y_host, token)

    print "Bambleweeny CLI Version " + b9y_cli_release + "\nConnected to " + b9y_instance
    commands = ['get','set']

    while True:
        cmd_input = raw_input("b9y v" + b9y_release + "> ")
        if cmd_input == "":
            continue
        items = shlex.split(cmd_input, posix=False)
        cmd = items[0]
        cmd_args1 = items[1:99]

        cmd_args = []
        for arg in cmd_args1:
            argstr = arg.strip('"')
            argstr = arg.strip("'")
            cmd_args.append(argstr)

        if cmd not in commands:
            print "??"
        #print "Command: " + cmd
        #print "Args: " + str(cmd_args)

        if cmd == 'get':
            b9y_get(b9y_host, token, cmd_args)

        if cmd == 'set':
            b9y_set(b9y_host, token, cmd_args)


if __name__ == '__main__':
    main()
