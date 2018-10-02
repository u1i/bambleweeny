endpoint=http://localhost:8080
echo $endpoint > endpoint.txt

# Create User
echo "Create User"
./create_user.sh

# Get Token
token=$(./get_user2_token.sh)

# Set Key Name and value
key=counter_$RANDOM
echo -e "\n\nKey is: $endpoint/keys/$key"

# Incr Key
echo -e "\n\nINCR key 10x"

for x in 1 2 3 4 5 6 7 8 9 10
do
	curl -X GET $endpoint/incr/$key -H "Authorization: Bearer $token"
	echo "..."
done
