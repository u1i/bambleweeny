for lang in python php ruby java javascript
do
	f=$(curl -X POST -H "Content-Type: application/json" -d '{"swaggerUrl":"https://raw.githubusercontent.com/u1i/bambleweeny/master/swagger.json"}' "http://generator.swagger.io/api/gen/clients/$lang" | tr "," "\n" | grep link | sed "s/\"}//;" | sed 's/.*":"//;' )

	curl -o $lang.zip $f

done
