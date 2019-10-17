<<<<<<< HEAD
endpoint=https://b9y.xwaay.net
echo $endpoint > endpoint.txt
=======
endpoint=$(cat endpoint.txt)
>>>>>>> a8e7b426c164272aa473ab283d59626a46064364

# Get Token
token=$(./get_user_token.sh)

# Set Key Name
key=perftest_write

echo -e "\n\nKey is: $endpoint/keys/$key"

# Performance Test: Write
ab -u create.txt -l -n 1000 -c 2 -T application/json -H "Authorization: Bearer $token" $endpoint/keys/$key
