![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

# Documentation Index

- [Getting Started](#getting-started)
- [Using Bambleweeny](#using-bambleweeny)
	- [HTTP/REST](#httprest)
	- [Command Line Interface](#command-line-interface)
	- [Client Libraries](#client-libraries)
	- [SDKs](#sdks)
- [Data Types & Concepts](#data-types-concepts)
	- [Users](#users)
		- [Admin](#admin)
		- [Users (Keyspaces)](#users-keyspaces)
	- [Authentication](#authentication)
	- [Keys](#keys)
		- [Set Keys](#set-keys)
		- [Read Keys](#read-keys)
		- [Increment Keys](#increment-keys)
	- [Routes](#routes)
		- [Create Routes](#create-routes)
		- [Access Routes](#access-routes)
		- [Dynamic Routes & Nested Keys](#dynamic-routes-nested-keys)
	- [Lists](#lists)
	- [Bins](#bins)
		- [Create Bins](#create-bins)
		- [Access Bins](#access-bins)

- [Running Bambleweeny](#running-bambleweeny)
	- [Standalone](#standalone)
	- [Separate Redis Backend](#separate-redis-backend)
	- [Topology](#topology)
	- [OpenShift](#openshift)
	- [Kubernetes](#kubernetes)
- [Configuration & Operations](#configuration-operations)
	- [Redis Connection](#redis-connection)
	- [Token Expiry](#token-expiry)
	- [Endpoints for info and db dump](#endpoints-for-info-and-db-dump)
		- [/info](#info)
		- [/save](#save)
	- [Static Settings](#static-settings)
		- [max\_request\_body\_size](#maxrequestbodysize)
		- [redis\_maxmemory](#redismaxmemory)
		- [redis\_datadir](#redisdatadir)


## Getting Started

New to Bambleweeny? This [Getting Started Guide](GettingStarted.md) shows you how to run it and do your first set of data operations.

## Using Bambleweeny

There are multiple ways of interacting with Bambleweeny. Whichever way you choose, all of them will use the [REST API](http://bambleweeny.sotong.io/) with OAuth and JSON over HTTP for communication. This makes it very easy to allow devices, apps and users inside and outside your firewall to access it.

### HTTP/REST

All functionality is available over the [REST API](http://bambleweeny.sotong.io/). It's an API first world! The /swagger endpoint gives you the [Swagger file](https://raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json).

### Command Line Interface

Perform commonly used operations in the [command-line interface](https://github.com/u1i/b9y-cli), available as binaries for [Windows](https://github.com/u1i/b9y-cli/raw/master/releases/b9y-cli-windows-amd64.zip), [MacOS](https://github.com/u1i/b9y-cli/raw/master/releases/b9y-cli-darwin-386.zip) and [Linux](https://github.com/u1i/b9y-cli/raw/master/releases/b9y-cli-linux-amd64.zip).

For example, entering `b9y-cli.exe -h http://10.158.27.88:8080` on a Windows machine connects you to Bambleweeny on a remote server using the default (admin) credentials.

### Client Libraries

The [b9y library](https://github.com/u1i/b9y-python) allows you to make Bambleweeny requests in Python.

`pip install b9y`

The [command-line interface](https://github.com/u1i/b9y-cli) makes use of it, so you could look at the code as an example.

Are you a .NET or JavaScript developer? We'd love your contribution to write a client library for those languages.

### SDKs

The following SDKs are auto-generated from the [Swagger file](https://raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json):

[Python](https://github.com/u1i/bambleweeny/raw/master/sdk/python.zip) | [Java](https://github.com/u1i/bambleweeny/raw/master/sdk/java.zip) | [Ruby](https://github.com/u1i/bambleweeny/raw/master/sdk/ruby.zip) | [PHP](https://github.com/u1i/bambleweeny/raw/master/sdk/php.zip) | [JavaScript](https://github.com/u1i/bambleweeny/raw/master/sdk/javascript.zip) | [Android](https://github.com/u1i/bambleweeny/raw/master/sdk/android.zip) | [HTML](https://github.com/u1i/bambleweeny/raw/master/sdk/html.zip)

## Data Types & Concepts

Bambleweeny gives you keys, lists, routes and bins. We'll cover all of these in the following section.

![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/datamodel1.png)

### Users

Unless exposed via routes (more on those below), all data is private to the respective individual users. Think of users rather like keyspaces.

#### Admin

The admin user (default credentials: admin/changeme) can create users, set quotas and get access to diagnostic information. Of course, the admin user has its own keyspace, too.

Create a user in the [CLI](https://github.com/u1i/b9y-cli):

`create_user user1 secret`

#### Users (Keyspaces)

Users have their individual keyspace and can, by default, create an unlimited number of resources.

### Authentication

Resources and general access to Bambleweeny are protected by an OAuth server. Before making requests and data operations, users must get a token using the /auth/token endpoint and provide as an `Authorization: Bearer` HTTP header in the subsequent requests. Tokens expire after 3000 seconds (default configuration).

Starting the [command-line interface](https://github.com/u1i/b9y-cli) without parameters will attempt a connection on localhost:8080 using the default admin credentials. Parameters `-h` for hostname, `-u` for username and `-p` for the password can be specified to use those instead. The command `token` in the [command-line interface](https://github.com/u1i/b9y-cli) will print the token to STDOUT for your convenience.

### IMPORTANT SECURITY NOTE

Passwords are stored as hash inside Redis using a default 'salt' – you should set an environment variable with a custom value (see below), otherwise session hijacking is possible. 

### Keys

Keys represent the essential data type in Bambleweeny as a key-value store. Valid key names are e.g. `foo`, `my_key788`, and `system:debug:level`.

#### Set Keys

In the [CLI](https://github.com/u1i/b9y-cli) you can issue `set foo bar` to create a key called `foo` with the value `bar`, or `set foo 'hello, world!'` for values that include spaces. Do this for simple content only, and use the REST API in Postman or from your application to add complex or UTF-8 encoded data.

Bambleweeny can handle binary content as well (however, the payload size is currently limited to 50kb):

`curl --upload-file image.png http://b9y/keys/pic -H AUTH`

#### Read Keys

To read the key you can use `get key` or make the following (authenticated) HTTP request:

`curl http://<host>:<port>/keys/foo -H 'Authorization: Bearer <token>`

#### Increment Keys

`incr mykey` increases a numeric key by 1 and returns it. If the key does not exist, it will be created and the operation returns `1`.

### Routes

Routes allow users to 'expose' keys and make them publicly available without the need for authentication. This is very useful if you want Bambleweeny to act as a web cache, mock API endpoints or simply share specific pieces of data within your distributed systems.

#### Create Routes

Using the [CLI](https://github.com/u1i/b9y-cli), the following set of commands create a key, exposes it over HTTP with the content type application/json and returns the newly created endpoint:

`set api '{"message": "hello"}'`   
`route api 'application/json;charset=utf-8'`

> /routes/125e6a6f-c3f3-403b-b096-89978773139b

#### Access Routes

`curl -i http://<host>:<port>/routes/125e6a6f-c3f3-403b-b096-89978773139b`
> Content-Type: text/html
> {"message": "hello"}

#### Dynamic Routes & Nested Keys

Nested keys give you greater flexibility to produce dynamic content. You can reference a key as `!@[mykey]` inside the value of another key. Let's make the previous example more interesting:

`set api '{"message": "!@[message]"}'`   
`set message 'cool stuff!'`   
`route api 'application/json;charset=utf-8'`

Routes are parsed dynamically, so the cURL command will return
> {"message": "cool stuff!"}

### Lists

Lists can store multiple values in one key, you use a `push` command to add an item and `pop` to retrieve an item. Retrieving an item also removes it from the list:

`push mylist cat`   
`push mylist dog`   
`pop mylist`   
> cat.

`pop mylist`   
> dog

`pop mylist`   
> None

Lists can be used to implement messaging queues. Reading from the queue removes the message. A future version might see a mechanism to properly dequeue it.

### Bins

Bins are endpoints that allow non-authenticated access to POST data, which is added to a list. You can use this mechanism to create event logs, webhooks, or collect form data.

#### Create Bins

Using the [CLI](https://github.com/u1i/b9y-cli), the following command creates a bin, exposes it over HTTP and returns the newly created endpoint:

`bin my_list`

> /bins/125e6a6f-c3f3-403b-b096-89978773139b

#### Access Bins

Anybody who knows the endpoint URL of the bin can post data to it:

`echo hello | curl -X POST -d@- http://<host>:<port>/bins/125e6a6f-c3f3-403b-b096-89978773139b`

The owner of the bin can then use `pop` commands to retrieve an element:

`pop my_list`

## Running Bambleweeny
### Standalone

`docker run -d -p 8080:8080 u1ih/bambleweeny`

This gives you a single, stateful and self-contained instance. Good enough for demos and tests.

Want to run it on a Raspberry Pi?

`docker run -d -p 8080:8080 u1ih/bambleweeny:arm-latest`

[Image on DockerHub](https://hub.docker.com/r/u1ih/bambleweeny/tags/) | [Dockerfile](Dockerfile)

### Separate Redis Backend

Bambleweeny uses Redis as an in-memory database. See below how to configure an external Redis connection using environment variables.

### Topology

![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/b9yms2.png)

How about running this as a topology instead, with one Redis container and one (and then later more) instances of b9y? Assuming you have Docker and docker-compose installed, simply run this command:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

You can modify the [docker-compose.yml](docker-compose.yml) file to your needs.

### OpenShift

Deploy a single instance of Bambleweeny on OpenShift:

1. **Deployment**   
`oc new-app u1ih/bambleweeny`   

1. **Expose**   
`oc expose svc/bambleweeny`

### Kubernetes

1. **Deployment**   
`kubectl run b9y --image=u1ih/bambleweeny:latest --env="redis_host=172.17.0.1" --env "redis_port=6379" --port=8080`

1. **Create a Service**  
`kubectl expose deployment b9y --type=NodePort`

1. **Scale up to 5 replicas**   
`kubectl scale deployments/b9y --replicas=5`

1. **Show the endpoint**   
`kubectl get services | grep b9y`

## Configuration & Operations

There are several ways to configure Bambleweeny and modify the default settings.

### Redis Connection

By default, b9y rund in 'Lite' mode which essentially starts an embedded Redis engine inside the container. This is good enough for many use cases, but you may want to point it to a 'proper' Redis environment instead. You can do this by setting environment variables:

`docker run [...] -e redis_host=localhost -e redis_port=6379 u1ih/bambleweeny:latest`

### Secret Salt

If you run b9y in a public environment you should provide an environment variable `salt` to increase the security and avoid potential session hijacking:

`docker run [...] -e salt=MYSECRET u1ih/bambleweeny:latest`

### Token Expiry

Provide an environment variable `token_expiry` that overrides the default token expiry of 3000 seconds:

`docker run [...] -e token_expiry=999999999 u1ih/bambleweeny:latest`

### Endpoints for info and db dump

The authenticated admin user can trigger the following endpoints:

#### /info

Provides detailed information on the Redis connection

#### /save

Triggers a 'save' on the Redis side, which dumps the content of the in-memory database to disk. You can map the directory to your host (and persist the data) by running b9y the following way:

`docker run [...] -v data:/data u1ih/bambleweeny:latest`

### Static Settings

The following settings are currently not configurable:

#### max\_request\_body\_size
Messages cannot be larger than 50kb (set in server.py CherryPy config)

#### redis\_maxmemory
Limit currently at 256 MB

#### redis\_datadir
Set to /data
