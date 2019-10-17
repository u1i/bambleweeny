endpoint=$(cat endpoint.txt)
adminpassword=$(cat adminpassword.txt)

curl -s -X POST \
  "$endpoint/auth/token?raw" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
<<<<<<< HEAD
  "password": "XXX"
=======
  "password": "'''$adminpassword'''"
>>>>>>> a8e7b426c164272aa473ab283d59626a46064364
}'
