curl -X PUT \
  http://localhost:8080/users/3 \
  -H 'Authorization: Bearer YWRtaW4=.MTUzNjg1MzQzNg==' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 419ecd0d-80a4-4699-a1a9-9a2040c8cc2b' \
  -d '{
  "quota": "19"
}'
