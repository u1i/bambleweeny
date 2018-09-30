# Get Token

token=$(./get_admin_token.sh)

key=key_$RANDOM

echo $key

# Write Key
echo $RANDOM | curl -X PUT -d @- http://localhost:8080/keys/$key -H "Authorization: Bearer $token"

# Get Key
curl http://localhost:8080/keys/$key -H "Authorization: Bearer $token"
