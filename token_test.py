from bwy_functions import issue_token, get_token_data

secret = "cX81bO0D"
token = issue_token(user="uli", id=17, expiry=60, salt=secret)

print "Got token:"
print token

d = get_token_data(token=token, salt=secret)

print d["error"]
