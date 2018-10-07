#!/usr/bin/env python
from sys import argv
import json, signal, shlex
from cmd import Cmd
from b9y import B9y

b9y_cli_release = "0.1.14"
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

class b9y_prompt(Cmd):
    try:
        args = getopts(argv)
    except:
        exit(1)

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

    b9y = B9y(b9y_host, b9y_user, b9y_password)
    b9y_instance, b9y_release = b9y.info()

    print("Bambleweeny CLI Version " + b9y_cli_release + "\nConnected to " + b9y_instance + " as " + b9y_user)

    prompt = "b9y v" + str(b9y_release) + "> "
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye!")
        return True

    def help_exit(self):
        print('Exit the application.')

    def do_set(self, inp):
        items = shlex.split(inp, posix=False)
        r = self.b9y.set(items[0], items[1])
        if r:
            print("OK")

    def do_incr(self, inp):
        items = shlex.split(inp, posix=False)
        r = self.b9y.incr(items[0])
        if r != None:
            print(str(r))
        else:
            print("Error")

    def do_get(self, inp):
        items = shlex.split(inp, posix=False)
        r = self.b9y.get(items[0])
        print(str(r))

    def help_set(self):
        print("Set a Key. Example: set foo bar")

    def help_get(self):
        print("Get a Key. Example: get foo")

    def help_incr(self):
        print("Increase Counter. Example: incr ticket_number")

    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)

        print "No idea what you want here. Type 'help' for available commands."

def main():
    signal.signal(signal.SIGINT, signal_handler)
    b9y_prompt().cmdloop()

if __name__ == '__main__':
    main()
