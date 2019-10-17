# Get Admin Token
endpoint=$(cat endpoint.txt)
token=$(./get_admin_token.sh)

# Create User

curl -X POST \
<<<<<<< HEAD
  https://b9y.xwaay.net/users \
=======
  $endpoint/users \
>>>>>>> a8e7b426c164272aa473ab283d59626a46064364
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "me",
  "password": "changeme"
}'
