#!/usr/bin/env python
from sys import argv
import requests, json, signal, shlex
from cmd import Cmd

b9y_cli_release = "0.1.7"
default_user = "admin"
default_password = "changeme"
default_host="http://localhost:8080"
debug = False

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

def b9y_help():
    print '''
Commands:

set - Set Key
Example: set foo bar
Example: set system:debug True
Example: set mydata '{"id": "331", "name": "Jane"}'

get - get a Key
Example: get foo
    '''

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
        print "ERROR: key invalid? Quota exceeded? (" + str(response.status_code) + ")"

def b9y_push(h, t, args):
    if len(args) != 2:
        print "ERROR: expecting exactly 2 argument, " + str(len(args)) + " given"
        return

    url = h + "/lists/" + args[0]
    headers = {'Authorization': "Bearer:" + t}
    payload = args[1]
    response = requests.request("POST", url, data=payload, headers=headers)

    if response.status_code == 200:
        print "OK"
    else:
        print "ERROR: key invalid? Quota exceeded? (" + str(response.status_code) + ")"

def b9y_incr(h, t, args):
    if len(args) != 1:
        print "ERROR: expecting exactly 2 argument, " + str(len(args)) + " given"
        return

    url = h + "/incr/" + args[0]
    headers = {'Authorization': "Bearer:" + t}
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print response.text
    else:
        print "ERROR: key invalid? Quota exceeded? (" + str(response.status_code) + ")"

class b9y_prompt(Cmd):
    try:
        args = getopts(argv)
    except:
        exit(1)

    global b9y_host
    global token

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

    print "Bambleweeny CLI Version " + b9y_cli_release + "\nConnected to " + b9y_instance + " as " + b9y_user

    prompt = "b9y v" + str(b9y_release) + "> "
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye!")
        return True

    def help_exit(self):
        print('Exit the application.')

    def do_set(self, inp):
        items = shlex.split(inp, posix=False)
        b9y_set(b9y_host, token, items)

    def do_incr(self, inp):
        items = shlex.split(inp, posix=False)
        b9y_incr(b9y_host, token, items)

    def do_get(self, inp):
        items = shlex.split(inp, posix=False)
        b9y_get(b9y_host, token, items)

    def help_set(self):
        print("Set a Key. Example: set foo bar")

    def help_get(self):
        print("Get a Key. Example: get foo")

    def help_incr(self):
        print("Increase Counter. Example: incr ticket_number")

    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)

    #do_EOF = do_exit
    #help_EOF = help_exit

def main():
    signal.signal(signal.SIGINT, signal_handler)
    b9y_prompt().cmdloop()

if __name__ == '__main__':
    main()
