endpoint=$(cat endpoint.txt)
token=$(./get_admin_token.sh)

curl -X PUT $endpoint/config/admin -H "Authorization: Bearer $token" -d '{
  "password": "newpassword" }'
