from bottle import Bottle, request, view, response
import json, os, uuid, base64, redis, time, hmac, hashlib, random

# Settings
admin_password = u"changeme"
secret_salt = "iKm4SyH6JCtA8l"
token_expiry_seconds = 3000

app = Bottle()

# The default path renders a hello world JSON message
@app.get('/')
def get_home():
	return(dict(msg="This is bambleweeny."))

# Default 404 handler
@app.error(404)
def error404(error):
    #return 'Nothing here, sorry'
	return("Nothing here.")

# Default 405 handler
@app.error(405)
def error405(error):
    #return 'Nothing here, sorry'
	return("Method not allowed for this endpoint.")

# Get Auth Token
@app.route('/auth/token', method='POST')
def get_token():

	# Get JSON Payload
	try:
		payload = json.load(request.body)

		username = payload["username"]
		password = payload["password"]
		#hash_object = hashlib.sha1(password)
		#pwhash = hash_object.hexdigest()
		pwhash = _get_password_hash(password)
	except:
		response.status = 400
		return dict({"message":"No valid JSON found in post body or mandatory fields missing."})

	user_list = rc.scan_iter("USER:*")
	for user in user_list:
		user_record = json.loads(rc.get(user))
		if user_record["email"] == username and user_record["hash"] == pwhash:
			user_token = _issue_token(user=username, id=user[5:], expiry=token_expiry_seconds, salt=secret_salt)
			if 'raw' in request.query:
				return(user_token)
			else:
				return(dict(token_type="bearer", access_token=user_token))

	response.status = 401
	return(dict(info="could not authorize user"))

# Test Auth Token
@app.route('/auth/test', method='GET')
def validate_token():

	d = _authenticate()
	return(dict(d))

# Create User
@app.route('/users', method='POST')
def create_user():

	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	try:
		payload = json.load(request.body)

		username = payload["email"]
		password = payload["password"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	if _find_email(username) == "found":
		response.status = 400
		return dict({"info":"A user with this email address exists already."})

	# Set ID and password hash for user
	new_userid = rc.incr("_USERID_")
	#hash_object = hashlib.sha1(password)
	#pwhash = hash_object.hexdigest()
	pwhash = _get_password_hash(password)

	user_record = {}
	user_record["email"] = username
	user_record["hash"] = pwhash
	user_record["quota"] = "0"

	rc.set("USER:"+str(new_userid), json.dumps(user_record, ensure_ascii=False))

	return(dict(info="created", id=new_userid))

# Read User
@app.route('/users/<id:int>', method='GET')
def get_user_details(id):

	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Read from Redis
	try:
		user_record = json.loads(rc.get("USER:"+str(id)))
	except:
		response.status = 404
		return dict({"info":"Not found."})

	user_out = {}
	user_out["email"] = user_record["email"]
	user_out["quota"] = user_record["quota"]

	return(dict(user_out))

# Set Quota for User
@app.route('/users/<id:int>', method='PUT')
def get_user_details(id):

	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get Payload
	try:
		payload = json.load(request.body)

		quota = payload["quota"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	# Read from Redis
	try:
		user_record = json.loads(rc.get("USER:"+str(id)))
	except:
		response.status = 404
		return dict({"info":"Not found."})

	user_record["quota"] = quota
	rc.set("USER:"+str(id), json.dumps(user_record, ensure_ascii=False))

	return dict({"info":"Quota updated for user."})

# Delete User
@app.route('/users/<id:int>', method='DELETE')
def delete_user(id):

	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Do not allow deleting admin
	if id == 0:
		response.status = 400
		return dict({"info":"Cannot delete admin user."})

	# Does the user exist?
	if rc.get("USER:"+str(id)) == None:
		response.status = 404
		return dict({"info":"Not found."})

	# Delete user record
	rc.delete("USER:"+str(id))
	return(dict(info="user deleted"))

# List All Users
@app.route('/users', method='GET')
def list_user():

	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	output = []
	user_list = rc.scan_iter("USER:*")
	for user in user_list:
		user_record = json.loads(rc.get(user))
		user_out = {}
		user_out["id"] = user[5:]
		user_out["email"] = user_record["email"]
		user_out["quota"] = user_record["quota"]
		output.append(user_out)

	return(dict(users=output))

# Change Admin Password
@app.route('/config/admin', method='PUT')
def set_admin_password():

	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	try:
		payload = json.load(request.body)
		new_password = payload["password"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	# Read record for admin user
	admin_record = json.loads(rc.get("USER:0"))

	# Hash and write new password
	#hash_object = hashlib.sha1(new_password)
	#admin_record["hash"] = hash_object.hexdigest()

	admin_record["hash"] = _get_password_hash(new_password)
	rc.set("USER:0", json.dumps(admin_record, ensure_ascii=False))

	return(dict(info="updated"))

# Create Resource
@app.route('/resources', method='POST')
def create_res():

	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID and quota
	user_id = api_auth["id"]
	user_quota = _get_user_quota(user_id)

	current_number_of_resources = _user_resources_number(user_id)

	# Are we allowed to create more objects?
	if user_quota != 0 and current_number_of_resources >= user_quota:
		response.status = 400
		return dict({"info":"Quota exceeded."})

	try:
		payload = json.load(request.body)
		content = payload["content"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	# Create uuid
	new_resource_id = uuid.uuid4()

	resource_record = {}
	resource_record["content"] = content

	rc.set("RES:"+str(user_id)+"::"+str(new_resource_id), json.dumps(resource_record, ensure_ascii=False))

	# Increase the counter of resources for this user_record
	rc.incr("NUMRES:"+str(user_id))

	return(dict(info="created", id=str(new_resource_id)))

# Get Resource
@app.route('/resources/<id>', method='GET')
def get_res(id):

	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# If authenticated as admin, we need to search for the resource first
	if api_auth["admin"] == "True":
		r = _find_resource(id)
		user_id = r["owner"]

	# Construct Resource Location from user_id and id
	redis_key = "RES:"+str(user_id)+"::"+str(id)

	# Read from Redis
	try:
		# resource_record = json.loads(rc.get("RES:"+str(user_id)+":"+str(id)))
		resource_record = json.loads(rc.get(redis_key))
	except:
		response.status = 404
		return dict({"info":"Not found."})

	res_out = {}
	res_out["content"] = resource_record["content"]

	return(dict(res_out))

# List All Resources
@app.route('/resources', method='GET')
def get_all_res():

	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Construct Resource Location
	redis_key = "RES:"+str(user_id)+":*"

	# Resource Location is different for admin access
	# Since in that case we want all resources
	if api_auth["admin"] == "True":
		redis_key = "RES:*"

	output = []
	resources_list = rc.scan_iter(redis_key)
	for res in resources_list:

		res_obj={}
		pos = res.find("::")
		pos1 = res.find(":")
		res_obj["id"] = res[pos+2:]
		res_obj["owner"] = res[pos1+1:pos]
		res_obj["acl"] = "nil"
		output.append(res_obj)

	return(dict(resources=output))

# Delete Resource
@app.route('/resources/<id>', method='DELETE')
def del_res(id):

	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# If authenticated as admin, we need to search for the resource first
	if api_auth["admin"] == "True":
		r = _find_resource(id)
		user_id = r["owner"]

	# Construct Resource Location
	redis_key = "RES:"+str(user_id)+"::"+str(id)

	# Does the resource exist?
	if rc.get(redis_key) == None:
		response.status = 404
		return(dict(info="not found"))

	# Delete from Redis
	try:
		rc.delete(redis_key)
	except:
		response.status = 404
		return(dict(info="not found"))

	# Decrease the counter of resources for this user_record
	rc.decr("NUMRES:"+str(user_id))

	return(dict(info="deleted", id=str(id)))

####### Helper functions

def _get_password_hash(pw):

	hash_object = hashlib.sha1(pw+secret_salt)
	return(hash_object.hexdigest())

def _create_admin():

	#hash_object = hashlib.sha1(admin_password)
	#pwhash = hash_object.hexdigest()
	pwhash = _get_password_hash(admin_password)
	user_record = {}
	user_record["email"] = "admin"
	user_record["hash"] = pwhash
	user_record["quota"] = "0"

	rc.set("USER:0", json.dumps(user_record, ensure_ascii=False))

	return

def _find_email(email):

        user_list = rc.scan_iter("USER:*")
        for user in user_list:
                user_record = json.loads(rc.get(user))
                if user_record["email"] == email:
                        return("found")

        return("not found")

def _find_resource(id):

	result={}
	result["error"] = "0"
	result["id"] = "-1"
	result["owner"] = "-1"

	try:
		redis_find = rc.scan_iter("*"+str(id))
		found_id = redis_find.next()
		result["id"] = found_id
		pos = found_id.find("::")
		pos1 = found_id.find(":")
		result["owner"] = found_id[pos1+1:pos]

	except:
		result["error"] = "1"

	return(result)

def _get_user_quota(uid):

	user_record = json.loads(rc.get("USER:"+str(uid)))

	return int(user_record["quota"])

def _user_resources_number(uid):

	n = rc.get("NUMRES:"+str(uid))
	if n == None:
		return 0
	else:
		return(int(n))

def _issue_token(user, expiry, id, salt):

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

def _get_token_data(token, salt):
    token_data = {}
    token_data["error"] = "0"
    token_data["admin"] = "False"
    token_data["authenticated"] = "False"

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

def _authenticate():
	bearer = request.environ.get('HTTP_AUTHORIZATION','')
	access_token=bearer[7:]

	# Extract the data from the token
	data = _get_token_data(token=access_token, salt=secret_salt)

	# If there was an error, end here
	if data["error"] != "0":
		return(dict(data))

	# Is the access token still valid?
	token_timestamp = data["timestamp"]
	current_time = int(time.time())
	delta = current_time - token_timestamp
	if delta > token_expiry_seconds:
		# expired
		data["authenticated"] = "False"
		data["info"] = "Token expired"
	else:
		# valid
		data["authenticated"] = "True"
		data["info"] = "Session expires in " + str(token_expiry_seconds - delta) + " seconds."

	# Set response header: username
	response.headers["B9Y-AUTHENTICATED-USER"] = data["user"]

	return(dict(data))

# Initialization
if not "redis_host" in os.environ or not "redis_port" in os.environ:
	exit("ERROR: please set the environment variables for Redis host")

# Connect to the Redis backend
redis_host = os.environ['redis_host']
redis_port = os.environ['redis_port']
rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

# Create record for admin user if it doesn't exist
if rc.get("USER:0") == None:
	_create_admin()
