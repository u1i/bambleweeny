endpoint=http://localhost:8080
echo $endpoint > endpoint.txt

# Create User
echo "Create User"
./create_user.sh

# Get Token
token=$(./get_user_token.sh)

# Upload
echo -e "\nUpload image.png"
curl --upload-file image.png $endpoint/keys/file -H "Authorization: Bearer $token" 

# Download
echo -e "\nDownload and save to /tmp/out.png"
curl -o /tmp/out.png -s $endpoint/keys/file -H "Authorization: Bearer $token"

echo -e "\n"
ls -l image.png
ls -l /tmp/out.png
