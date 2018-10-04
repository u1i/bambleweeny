![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

# b9y-cli - Commandline Client

A client for [Bamblweeny](https://github.com/u1i/bambleweeny) for the command line.

## Install
pip install b9y-cli

## Run

Run `b9y-cli` on the shell to connect using the default credentials (admin/changeme on localhost:8080).

Alternatively, you can specify the connection parameters like this:

`b9y-cli -u my_user1`  
`b9y-cli -h http://myhost:8080 -u me -p secret`  
`b9y-cli -h https://b9y.myhost.com`

## Using the CLI

You should see a prompt like the following:

![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/cli2.jpg)

Now you can use get and set commands:

`set foo bar`
> OK

`get foo`
> bar

## PyPi

[b9y-cli on pypi](https://pypi.org/project/b9y-cli/)
