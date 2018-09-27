#!/bin/sh

if [ "$b9y_mode" = "lite" ]
then
  echo "Starting embedded Redis instance"
  export redis_host=localhost
  export redis_port=6379
  /usr/bin/redis-server &
fi

python /app/server.py
