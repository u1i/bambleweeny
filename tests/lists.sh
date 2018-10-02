endpoint=http://localhost:8080
echo $endpoint > endpoint.txt

# Create User
echo "Create User"
./create_user.sh

# Get Token
token=$(./get_user_token.sh)

# Set List Name
list=testlist_$RANDOM
echo -e "\n\nList is: $endpoint/lists/$list"

for x in $(seq 20)
do
curl -X POST \
  $endpoint/lists/$list \
  -H "Authorization: Bearer $token" \
  -d "$RANDOM"
done
