# Get Admin Token

token=$(./get_admin_token.sh)

# Create User

curl -X POST \
  https://b9y.xwaay.net/users \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "me",
  "password": "changeme"
}'
