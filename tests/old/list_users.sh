token=$(./get_admin_token.sh)

curl -X GET \
  http://localhost:8080/users \
  -H "Authorization: Bearer $token" \
  -H 'Cache-Control: no-cache' \
  -H 'Postman-Token: 008d651a-1d43-48c4-93a5-1fdeb080b21c'
