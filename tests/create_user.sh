curl -X POST \
  http://localhost:8080/users \
  -H 'Authorization: Bearer YWRtaW4=.MTUzNjgzMjA2OA==' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "me@privacy.net",
  "password": "changeme"
}'
