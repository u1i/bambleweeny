endpoint=http://localhost:8080
echo $endpoint > endpoint.txt

# Create User
echo "Create User"
./create_user2.sh

# Get Token
token=$(./get_user2_token.sh)

curl -s $endpoint/auth/test -H "Authorization: Bearer $token" 
