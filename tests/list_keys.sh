endpoint=http://localhost:8080
echo $endpoint > endpoint.txt

# Get Token
token=$(./get_admin_token.sh)

# Get Key
curl -s $endpoint/keys -H "Authorization: Bearer $token"

