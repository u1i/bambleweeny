curl -X POST \
  http://localhost:8080/resources \
  -H 'Authorization: Bearer eyJpIjogIjYiLCAidSI6ICJtZUBwcml2YWN5Lm5ldCIsICJ0IjogIjE1MzY5MjkyNjIifQ==.fa23f260ef7e7ede23a7711f4c9dfa3fbbfd055db53e23df8424828d52bf374e' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: d50c277d-fabb-4eb2-8541-5d6e5d08685b' \
  -d '{
  "content": "lorem ipsum"
}'
