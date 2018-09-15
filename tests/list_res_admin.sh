token=$(./get_admin_token.sh)

curl -X GET \
  http://localhost:8080/resources \
  -H "Authorization: Bearer $token " \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json'
