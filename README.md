![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy_small.png)

Bambleweeny is a versatile, lightweight database system that offers a REST API along with identity, access &amp; quota management. Written in Python, using a Redis backend, deployable in a tiny container. Life is great!

## Project Status

[x] OAuth flow & Access Management  
[x] Admin Access  
[x] User Access  
[x] Quota Management  
[ ] *Resources*

## Deploy using Docker Compose

[Image on DockerHub](https://hub.docker.com/r/u1ih/bambleweeny/tags/) | [Dockerfile](Dockerfile) | [docker-compose.yml](docker-compose.yml) 

Assuming you have Docker and docker-compose installed, simply run this command:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

Bambleweeny should then be available at `http://localhost:8080`


## REST API

[Swagger File](https://github.com/u1i/bambleweeny/blob/master/swagger.json) | [Swagger UI](http://bambleweeny.sotong.io/)

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

