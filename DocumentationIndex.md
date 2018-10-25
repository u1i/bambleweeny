![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

# Documentation Index

## Using Bambleweeny
### HTTP/REST
### Command Line Interface
### Client Libraries

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
#### Access Routes
#### Dynamic Routes & Nested Keys
### Lists

## Running Bambleweeny
### Standalone
### Redis Backend
### OpenShift
### Kubernetes

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
