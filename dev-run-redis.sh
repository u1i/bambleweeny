docker rm bw-redis 2>/dev/null
docker run --name bw-redis -d -p 6379:6379 redis
