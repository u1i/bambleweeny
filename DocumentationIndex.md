![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

# Documentation Index

## Getting Started

[Getting Started Guide](GettingStarted.md)

## Using Bambleweeny
### HTTP/REST
### Command Line Interface
### Client Libraries
### SDKs

[Python](https://github.com/u1i/bambleweeny/raw/master/sdk/python.zip) | [Java](https://github.com/u1i/bambleweeny/raw/master/sdk/java.zip) | [Ruby](https://github.com/u1i/bambleweeny/raw/master/sdk/ruby.zip) | [PHP](https://github.com/u1i/bambleweeny/raw/master/sdk/php.zip) | [JavaScript](https://github.com/u1i/bambleweeny/raw/master/sdk/javascript.zip) | [Android](https://github.com/u1i/bambleweeny/raw/master/sdk/android.zip) | [HTML](https://github.com/u1i/bambleweeny/raw/master/sdk/html.zip)

## Data Types & Concepts

### Users
#### Admin
#### Users (Keyspaces)
### Authentication
### Keys
#### Set Keys
#### Read Keys
#### Increment Keys
### Routes
#### Create Routes

`set api '{"message": "hello"}'`
`route api 'application/json;charset=utf-8'`

> /routes/125e6a6f-c3f3-403b-b096-89978773139b

#### Access Routes

`curl http://b9y/routes/125e6a6f-c3f3-403b-b096-89978773139b`
> {"message": "hello"}

#### Dynamic Routes & Nested Keys
### Lists

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

[Run on OpenShift](openshift-run.sh)

### Kubernetes

[Run on Kubernetes](kube-run.sh)

## Configuration & Operations

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
