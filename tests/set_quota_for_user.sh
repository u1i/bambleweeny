endpoint=$(cat endpoint.txt)

# Get Admin Token

token=$(./get_admin_token.sh)

curl -X PUT $endpoint/users/1 -H "Authorization: Bearer $token" \
  -H 'Content-Type: application/json' \
  -d '{
  "quota": "30"
}'
