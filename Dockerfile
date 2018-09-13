FROM alpine
MAINTAINER uli.hitzel@gmail.com

EXPOSE 8080

RUN apk update
RUN apk add python2
RUN apk add py-pip
RUN mkdir /app
RUN pip install cherrypy bottle
COPY views /app/views
RUN ln -s /app/views /views
COPY server.py /app/server.py
COPY my_bottle_app.py /app/my_bottle_app.py

CMD ["python","/app/server.py"]
