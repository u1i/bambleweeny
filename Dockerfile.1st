FROM alpine
MAINTAINER uli.hitzel@gmail.com

EXPOSE 8080

RUN apk update
RUN apk add python2
RUN apk add py-pip
RUN mkdir /app
RUN pip install cherrypy bottle redis
COPY server.py /app/server.py
COPY bambleweeny.py /app/bambleweeny.py

CMD ["python","/app/server.py"]
