# Get Token

token=$(./get_user_token.sh)

ab -p create.txt -l -n 1000 -c 2 -T application/json -H "Authorization: Bearer $token" http://127.0.0.1:8080/resources
