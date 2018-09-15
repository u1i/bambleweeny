# Get Token

token=$(./get_user_token.sh)

# Create Resource
out=$(curl -sS -X POST \
  http://localhost:8080/resources \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: d50c277d-fabb-4eb2-8541-5d6e5d08685b' \
  -d '{
  "content": "lorem ipsum"
}' 2>/dev/null)

res=$(echo $out | tr "," "\n" | grep '"id"' | sed 's/"}//; s/.*"//;')

# curl -sS -H "Authorization: Bearer $token" http://localhost:8080/resources/$res 2>/dev/null

ab -n 1000 -c 4 -H "Authorization: Bearer $token" http://127.0.0.1:8080/resources/$res
