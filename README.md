![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy_small.png)

Bambleweeny is lightweight HTTP/REST based key-value store that offers identity, access & quota management. Written in Python, using a Redis backend, deployable in a tiny container. Life is great!

## Deploy using Docker

[Image on DockerHub](https://hub.docker.com/r/u1ih/bambleweeny/tags/) | [Dockerfile](Dockerfile) | [docker-compose.yml](docker-compose.yml) 

Assuming you have Docker and docker-compose installed, simply run this command:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

Bambleweeny should then be available at `http://localhost:8080` and you can create resources using HTTP requests like the following:

`curl -X POST http://localhost:8080/resources -H AUTH -d '{"content": "lorem ipsum"}'`

Details on authentication and the endpoints below. The default password for admin is 'changeme'.

## REST API

[Swagger File](https://github.com/u1i/bambleweeny/blob/master/swagger.json) | [Swagger UI](http://bambleweeny.sotong.io/) | [Postman Collection](postman_collection.json) | [Postman Docu](https://documenter.getpostman.com/view/1926148/RWaKT8rF)

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

