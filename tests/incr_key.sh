# Get Token

token=$(./get_admin_token.sh)

key=q_$RANDOM

echo $key

# Incr Key

for x in 1 2 3 4 5
do
echo "..."
curl http://localhost:8080/incr/$key -H "Authorization: Bearer $token"
done
