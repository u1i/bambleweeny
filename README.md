![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-270/) [![GitHub release](https://img.shields.io/github/release/u1i/bambleweeny.svg)](https://GitHub.com/u1i/bambleweeny/releases) [![Docker Pulls](https://img.shields.io/badge/dynamic/json.svg?label=Docker%20Pulls&url=https%3A%2F%2Fhub.docker.com%2Fv2%2Frepositories%2Fu1ih%2Fbambleweeny%2F&query=$.pull_count&colorB=2)](https://hub.docker.com/r/u1ih/bambleweeny/) [![GitHub license](https://img.shields.io/github/license/u1i/bambleweeny.svg)](https://github.com/u1i/bambleweeny/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/u1i/bambleweeny.svg)](https://GitHub.com/u1i/bambleweeny/issues/) ![](https://img.shields.io/swagger/valid/2.0/https/raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json.svg)

Bambleweeny is lightweight HTTP/REST based key-value store that offers identity, access & quota management. It's fast, easy to use, and well-documented.

Written in Python, using a Redis backend, deployable in a tiny container.

**Use cases**: data ingest for mobile / IOT, configuration management and coordination for distributed systems.

## Simple HTTP based Key/Value Access

### Get 'foo'

`curl http://b9y/keys/foo -H AUTH`

### Set 'foo' = 'bar'

`echo bar | curl -X PUT -d @- http://b9y/keys/foo -H AUTH`

### Create a counter - get a'queue number'

`curl http://b9y/incr/queue_number -H AUTH`

The [Getting Started Guide](GettingStarted.md) gives you detailed examples, and of course there's the [API Documentation](http://bambleweeny.sotong.io/).

### Performance (Apache Bench)

* **~45 reads per second, ~29 writes per second** - Raspberry Pi 3 Model B, ARMv7 1GB RAM
* **~540 reads per second, ~400 writes per second** - 1x vCPU 1 GB RAM (AWS t2.micro)
* **~800 reads per second, ~530 writes per second** - MacBook Pro 2.9GHz i7 16GB RAM

## Run Bambleweeny

`docker run -d -p 8080:8080 u1ih/bambleweeny`

This gives you a single, stateful and self-contained instance. Good enough for demos and tests.

Want to run it on a Raspberry Pi?

`docker run -d -p 8080:8080 u1ih/bambleweeny:arm-0.24`

## Deploy as a topology

![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/b9yms2.png)

[Image on DockerHub](https://hub.docker.com/r/u1ih/bambleweeny/tags/) | [Dockerfile](Dockerfile) | [docker-compose.yml](docker-compose.yml) | [Run on Kubernetes](kube-run.sh) | [Run on OpenShift](openshift-run.sh)

How about running this as a topology instead, with one Redis container and one (and then later more) instances of b9y? Assuming you have Docker and docker-compose installed, simply run this command:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

## Using the REST API

Check out the [Getting Started Guide](GettingStarted.md) and the [API Documentation](http://bambleweeny.sotong.io/) for detailed information on managing users and keys.

 [Swagger File](https://raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json) | [Postman Collection](docs/postman_collection.json) | [Postman Docu](https://documenter.getpostman.com/view/1926148/RWaKT8rF)

Download SDK: [Python](https://github.com/u1i/bambleweeny/raw/master/sdk/python.zip) | [Java](https://github.com/u1i/bambleweeny/raw/master/sdk/java.zip) | [Ruby](https://github.com/u1i/bambleweeny/raw/master/sdk/ruby.zip) | [PHP](https://github.com/u1i/bambleweeny/raw/master/sdk/php.zip) | [JavaScript](https://github.com/u1i/bambleweeny/raw/master/sdk/javascript.zip) | [Android](https://github.com/u1i/bambleweeny/raw/master/sdk/android.zip) | [HTML](https://github.com/u1i/bambleweeny/raw/master/sdk/html.zip)

[![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/crud4.png)](http://bambleweeny.sotong.io/)


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
