import base64, time, json, hmac, hashlib

def issue_token(user, expiry, id, salt):

    # Dict containing user info
    content={}
    content["u"] = user
    content["t"] = str(int(time.time()))
    content["i"] = id

    # Create base64 encoded version
    c = base64.urlsafe_b64encode(json.dumps(content))

    # Get an hmac signature
    hmac1 = hmac.new(salt, c, hashlib.sha256 )

    return(c + "." + hmac1.hexdigest())

def get_token_data(token, salt):
    token_data = {}
    token_data["error"] = "0"
    token_data["admin"] = "False"

    try:
        # Get base64 encoded content and the signature from the token
        separator = token.find(".")
        sig_token = token[separator+1:]
        content_raw = base64.urlsafe_b64decode(token[:separator])
        content = json.loads(content_raw)

        # Create signature
        c = base64.urlsafe_b64encode(json.dumps(content))
        hmac1 = hmac.new(salt, c, hashlib.sha256 )
        sig_check = hmac1.hexdigest()

        # Only get the data if the signature is valid
        if sig_token == sig_check:

            token_data["timestamp"] = int(content["t"])
            token_data["user"] = content["u"]
            token_data["id"] = content["i"]

            if content["u"] == 'admin':
                token_data["admin"] = "True"
        else:
            token_data["error"] = "1"
    except:
        token_data["error"] = "1"

    return(token_data)
