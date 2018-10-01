endpoint=$(cat endpoint.txt)

curl -s -X POST \
  "$endpoint/auth/token?raw" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
  "password": "changeme"
}'
