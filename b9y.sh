#!/bin/sh

# This script is the entry point for the Docker container
# Run an embedded Redis instance if Redis connection info is not provided
if [ "$redis_host" = "" ]
then
  echo "Starting embedded Redis instance"
  export redis_embedded=True
  export redis_host=localhost
  export redis_port=6379
  /usr/bin/redis-server --dbfilename dump.rdb --dir /data &
fi

python /app/server.py
