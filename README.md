![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-270/) [![GitHub release](https://img.shields.io/github/release/u1i/bambleweeny.svg)](https://GitHub.com/u1i/bambleweeny/releases) [![docker pulls](https://img.shields.io/badge/dynamic/json.svg?label=Docker%20Pulls&url=https%3A%2F%2Fhub.docker.com%2Fv2%2Frepositories%2Fu1ih%2Fbambleweeny%2F&query=$.pull_count&colorB=2)](https://hub.docker.com/r/u1ih/bambleweeny/) [![](https://img.shields.io/badge/documentation-index-green.svg)](https://github.com/u1i/bambleweeny/blob/master/DocumentationIndex.md) [![GitHub license](https://img.shields.io/github/license/u1i/bambleweeny.svg)](https://github.com/u1i/bambleweeny/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/u1i/bambleweeny.svg)](https://GitHub.com/u1i/bambleweeny/issues/) ![](https://img.shields.io/swagger/valid/2.0/https/raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json.svg)

Bambleweeny is a lightweight HTTP/REST based key-value store and message broker that offers identity, access & quota management. It's fast, easy to use, and well-documented.

Written in Python, using a Redis backend, deployable in a tiny container.

**Use cases**: web caching, data ingestion for mobile & IOT, mocking API endpoints, configuration management and coordination across distributed systems.

![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/b9y-logic7.png)

## Run Bambleweeny

`docker run -d -p 8080:8080 u1ih/bambleweeny`

This gives you a single, stateful and self-contained instance. Good enough for demos and tests. See the [Documentation Index](DocumentationIndex.md) for infos on how to run it as a topology, in Kubernetes and OpenShift.

## Simple HTTP based Key/Value Access

Bambleweeny has a nice [command-line interface](https://github.com/u1i/b9y-cli). Here we'll show you some cURL examples, since everything happens over HTTP:

### Get 'foo'

`curl http://b9y/keys/foo -H AUTH`

### Set 'foo' = 'bar'

`echo bar | curl -X PUT -d @- http://b9y/keys/foo -H AUTH`

### Make 'foo' public, so anyone can read

`echo '{"key":"foo", "content_type":"text/html"}' | curl -X POST -d @- http://b9y/routes -H AUTH`

> /routes/125e6a6f-c3f3-403b-b096-89978773139b

`curl http://b9y/routes/125e6a6f-c3f3-403b-b096-89978773139b`
> bar


### Upload binary files

`curl --upload-file image.png http://b9y/keys/pic -H AUTH`

### Create a counter - 'pick a number'

`curl http://b9y/incr/ticket_number -H AUTH`

## Message Broker

### Push a message to a queue

`echo test_message | curl -X POST http://b9y/lists/my_queue -H AUTH`

### Pop a message from a queue

`curl http://b9y/lists/my_queue -H AUTH`

The [Getting Started Guide](GettingStarted.md) helps you get going quickly.

## Using the REST API

The endpoint /swagger gives you the [Swagger file](https://raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json). Check out the [Getting Started Guide](GettingStarted.md) and the [API Documentation](http://bambleweeny.sotong.io/) for detailed information on managing users, keys and lists.
 
[![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/crud7.png)](http://bambleweeny.sotong.io/)

## Performance (Apache Bench)

* **~45 reads per second, ~29 writes per second** - Raspberry Pi 3 Model B, ARMv7 1GB RAM
* **~540 reads per second, ~400 writes per second** - 1x vCPU 1 GB RAM (AWS t2.micro)
* **~800 reads per second, ~530 writes per second** - MacBook Pro 2.9GHz i7 16GB RAM

## Behind the Scenes
### Design Principles:

* minimal use of external libraries
* readable code over performance
* simplicity over feature overload

### Stack & Tools

* Python, [Bottle](https://bottlepy.org/) WSGI Framework, [CherryPy](http://cherrypy.org/) thread-pooled webserver
* Redis
* Docker

*[Where does the name come from?](http://hitchhikers.wikia.com/wiki/Bambleweeny_57_Submeson_Brain)*
