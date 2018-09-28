FROM alpine
MAINTAINER uli.hitzel@gmail.com

EXPOSE 8080

RUN apk update
RUN apk add python2
RUN apk add py-pip
RUN apk update
RUN apk add redis
RUN mkdir /app
RUN pip install cherrypy bottle redis
COPY b9y.sh /app
COPY server.py /app/server.py
COPY bambleweeny.py /app/bambleweeny.py
COPY swagger.json /app/swagger.json

CMD ["/app/b9y.sh"]
