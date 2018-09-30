token=$(./get_admin_token.sh)

curl -X DELETE \
  http://localhost:8080/users/1 \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Postman-Token: d20c370b-501c-444c-ab11-1fa338311510'
