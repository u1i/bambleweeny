# Get Token

token=$(./get_user_token.sh)

# Create Resource
curl -i -X POST \
  http://localhost:8080/resources \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: d50c277d-fabb-4eb2-8541-5d6e5d08685b' \
  -d '{
  "content": "lorem ipsum"
}'
