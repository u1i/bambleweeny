# Bambleweeny - Commandline Client

A client for [Bamblweeny](https://github.com/u1i/bambleweeny) for the command line.


## PyPi

[b9y-cli on pypi](https://test.pypi.org/project/b9y-cli/)

## Install
pip install --index-url https://test.pypi.org/simple/ b9y-cli

## Run

Run `b9y-cli` on the shell to connect using the default credentials (admin/changeme on localhost:8080).

Alternatively, you can specify the connection parameters like this:

`b9y-cli -h https://myhost:8080 -u me -p secret`

## Using the CLI

You should see a prompt like the following:

> Bambleweeny CLI Version 0.01.

> Connected to 7adc879f.

> b9y v0.26>

Now you can use get and set commands:

`set foo bar`
> OK

`get foo`
> bar

