![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-270/) [![GitHub release](https://img.shields.io/github/release/u1i/bambleweeny.svg)](https://GitHub.com/u1i/bambleweeny/releases) [![Docker Pulls](https://img.shields.io/badge/dynamic/json.svg?label=Docker%20Pulls&url=https%3A%2F%2Fhub.docker.com%2Fv2%2Frepositories%2Fu1ih%2Fbambleweeny%2F&query=$.pull_count&colorB=2)](https://hub.docker.com/r/u1ih/bambleweeny/) [![](https://img.shields.io/badge/Commandline-tool-green.svg)](https://github.com/u1i/bambleweeny/tree/master/b9y-cli-package) [![GitHub license](https://img.shields.io/github/license/u1i/bambleweeny.svg)](https://github.com/u1i/bambleweeny/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/u1i/bambleweeny.svg)](https://GitHub.com/u1i/bambleweeny/issues/) ![](https://img.shields.io/swagger/valid/2.0/https/raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json.svg)

Bambleweeny is a lightweight HTTP/REST based key-value store and message broker that offers identity, access & quota management. It's fast, easy to use, and well-documented.

Written in Python, using a Redis backend, deployable in a tiny container.

**Use cases**: data ingest for mobile / IOT, configuration management and coordination across distributed systems.

## Simple HTTP based Key/Value Access

### Get 'foo'

`curl http://b9y/keys/foo -H AUTH`

### Set 'foo' = 'bar'

`echo bar | curl -X PUT -d @- http://b9y/keys/foo -H AUTH`

### Make 'foo' public, so anyone can read

`echo '{"key":"foo", "content_type":"application/json;charset=utf-8"}' | curl -X POST -d @- http://b9y/routes -H AUTH`

> /routes/125e6a6f-c3f3-403b-b096-89978773139b

`curl http://b9y/routes/125e6a6f-c3f3-403b-b096-89978773139b'
> bar


### Upload binary files

`curl --upload-file image.png http://b9y/keys/pic -H AUTH`

### Create a counter - 'pick a number'

`curl http://b9y/incr/queue_number -H AUTH`

## Message Broker

### Push a message to a queue

`echo test_message | curl -X POST http://b9y/lists/my_queue -H AUTH`

### Pop a message from a queue

`curl http://b9y/lists/my_queue -H AUTH`

The [Getting Started Guide](GettingStarted.md) gives you detailed examples, and of course there's the [API Documentation](http://bambleweeny.sotong.io/).

### Performance (Apache Bench)

* **~45 reads per second, ~29 writes per second** - Raspberry Pi 3 Model B, ARMv7 1GB RAM
* **~540 reads per second, ~400 writes per second** - 1x vCPU 1 GB RAM (AWS t2.micro)
* **~800 reads per second, ~530 writes per second** - MacBook Pro 2.9GHz i7 16GB RAM

## Run Bambleweeny

`docker run -d -p 8080:8080 u1ih/bambleweeny`

This gives you a single, stateful and self-contained instance. Good enough for demos and tests.

Want to run it on a Raspberry Pi?

`docker run -d -p 8080:8080 u1ih/bambleweeny:arm-0.26`

## Deploy as a topology

![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/b9yms2.png)

[Image on DockerHub](https://hub.docker.com/r/u1ih/bambleweeny/tags/) | [Dockerfile](Dockerfile) | [docker-compose.yml](docker-compose.yml) | [Run on Kubernetes](kube-run.sh) | [Run on OpenShift](openshift-run.sh)

How about running this as a topology instead, with one Redis container and one (and then later more) instances of b9y? Assuming you have Docker and docker-compose installed, simply run this command:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

## Using the CLI

Bambleweeny offers a commandline tool for easy access to data operations: [check it out here](https://github.com/u1i/bambleweeny/tree/master/b9y-cli-package).

## Python Bindings

`pip install b9y` gives you a [b9y library](https://pypi.org/project/b9y/) you can use in your application.

## Using the REST API

Check out the [Getting Started Guide](GettingStarted.md) and the [API Documentation](http://bambleweeny.sotong.io/) for detailed information on managing users, keys and lists.

 [Swagger File](https://raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json) | [Postman Collection](docs/postman_collection.json) | [Postman Docu](https://documenter.getpostman.com/view/1926148/RWaKT8rF)

Download SDK: [Python](https://github.com/u1i/bambleweeny/raw/master/sdk/python.zip) | [Java](https://github.com/u1i/bambleweeny/raw/master/sdk/java.zip) | [Ruby](https://github.com/u1i/bambleweeny/raw/master/sdk/ruby.zip) | [PHP](https://github.com/u1i/bambleweeny/raw/master/sdk/php.zip) | [JavaScript](https://github.com/u1i/bambleweeny/raw/master/sdk/javascript.zip) | [Android](https://github.com/u1i/bambleweeny/raw/master/sdk/android.zip) | [HTML](https://github.com/u1i/bambleweeny/raw/master/sdk/html.zip)

[![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/crud5.png)](http://bambleweeny.sotong.io/)

## Bamblweeeny Configuration & Operations

There are several ways to configure Bambleweeny and modify the default settings.

### Redis Connection

By default, B9y rund in 'Lite' mode which essentially starts an embedded Redis engine inside the container. This is good enough for many use cases, but you may want to point it to a 'proper' Redis environment instead. You can do this by setting environment variables:

`docker run [...] -e redis_host=localhost -e redis_port=6379 u1ih/bambleweeny:latest`

### Token Expiry

Provide an environment variable `token_expiry` that overrides the default token expiry of 3000 seconds:

`docker run [...] -e token_expiry=999999999 u1ih/bambleweeny:latest`

### Endpoints for info and db dump

The authenticated admin user can trigger the following endpoints:

#### /info

Provides detailed information on the Redis connection

#### /save

Triggers a 'save' on the Redis side, which dumps the content of the in-memory database to disk. You can map the directory to your host (and persist the data) by running B9y the following way:

`docker run [...] -v data:/data u1ih/bambleweeny:latest`

### Static Settings

The following settings are currently not configurable:

#### max\_request\_body\_size
Messages cannot be larger than 50kb (set in server.py CherryPy config)

#### redis\_maxmemory
Limit currently at 256 MB

#### redis\_datadir
Set to /data


## Behind the Scenes
### Design Principles:

* minimal use of external libraries
* readable code over performance
* prototype / educational nature

### Stack & Tools

* Python, [Bottle](https://bottlepy.org/) WSGI Framework, [CherryPy](http://cherrypy.org/) thread-pooled webserver
* Redis
* Docker

*[Where does the name come from?](http://hitchhikers.wikia.com/wiki/Bambleweeny_57_Submeson_Brain)*
