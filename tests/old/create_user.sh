# Get Admin Token

token=$(./get_admin_token.sh)

# Create User

curl -X POST \
  http://localhost:8080/users \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "me@privacy.net",
  "password": "changeme"
}'
