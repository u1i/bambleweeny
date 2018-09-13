curl -X POST \
  http://localhost:8080/auth/token \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: b3cf2aee-7740-463f-95aa-67c3d28cc024' \
  -d '{
  "username": "me@privacy.net",
  "password": "changeme"
}'
