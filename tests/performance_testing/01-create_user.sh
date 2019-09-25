# Get Admin Token
endpoint=$(cat endpoint.txt)
token=$(./get_admin_token.sh)

# Create User

curl -X POST \
  $endpoint/users \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "me",
  "password": "changeme"
}'
