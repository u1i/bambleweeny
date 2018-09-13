import base64, time

def issue_token(user, expiry):

    # Token has the format base64(username).base64(unix_timestamp)
    # To Do: add integrity check / hash

    u = base64.urlsafe_b64encode(user)
    t = base64.urlsafe_b64encode(str(int(time.time())))
    return(u + "." + t)

def get_token_data(token):
    token_data = {}
    token_data["error"] = "0"
    token_data["admin"] = "False"

    try:
        separator = token.find(".")
        token_data["user"] = base64.urlsafe_b64decode(token[:separator])
        token_data["timestamp"] = int(base64.urlsafe_b64decode(token[separator+1:]))

        if token_data["user"] == 'admin':
            token_data["admin"] = "True"

    except:
        token_data["error"] = "1"

    return(token_data)
