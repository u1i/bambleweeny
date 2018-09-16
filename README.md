![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

Bambleweeny is lightweight HTTP/REST based key-value store that offers identity, access & quota management. It's fast, easy to use, and well-documented.

Written in Python, using a Redis backend, deployable in a tiny container.

**Usage**:  
`curl -X POST http://bambleweeny/resources -d '{"content": "lorem ipsum"}' -H AUTH`


**Performance** (Apache Bench):

* **~300 reads per second, ~220 writes per second** - 1x vCPU 1GB RAM (linode)
* **~800 reads per second, ~520 writes per second** - 4x vCPU 32GB RAM (baremetal x1.small on packet)

Requests per second: ~800 (read) and ~450 (write)  

## Deploy using Docker

[Image on DockerHub](https://hub.docker.com/r/u1ih/bambleweeny/tags/) | [Dockerfile](Dockerfile) | [docker-compose.yml](docker-compose.yml) 

Assuming you have Docker and docker-compose installed, simply run this command:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

## Using the REST API

Check out the [Getting Started Guide](GettingStarted.md) for a detailed run-through for managing users and resources.

[Swagger File](https://github.com/u1i/bambleweeny/blob/master/swagger.json) | [Swagger UI](http://bambleweeny.sotong.io/) | [Postman Collection](postman_collection.json) | [Postman Docu](https://documenter.getpostman.com/view/1926148/RWaKT8rF)

Download SDK: [Python](https://github.com/u1i/bambleweeny/raw/master/sdk/python.zip) | [Java](https://github.com/u1i/bambleweeny/raw/master/sdk/java.zip) | [Ruby](https://github.com/u1i/bambleweeny/raw/master/sdk/ruby.zip) | [PHP](https://github.com/u1i/bambleweeny/raw/master/sdk/php.zip) | [JavaScript](https://github.com/u1i/bambleweeny/raw/master/sdk/javascript.zip) | [Android](https://github.com/u1i/bambleweeny/raw/master/sdk/android) | [HTML](https://github.com/u1i/bambleweeny/raw/master/sdk/html)

[![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/api.png)](http://bambleweeny.sotong.io/)


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
