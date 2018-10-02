endpoint=$(cat endpoint.txt)

curl -sS -X POST \
  "$endpoint/auth/token?raw" \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "me2@privacy.net",
  "password": "changeme"
}' 2>/dev/null
