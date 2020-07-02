import json, os, uuid, base64, redis, time, hmac, hashlib, keyword, re
from multiprocessing import Process
from bottle import Bottle, request, response

# Settings
admin_password = u"changeme"
default_salt = "iKm4SyH6JCtA8l"
default_token_expiry_seconds = 3000
redis_datadir = '/data' # this is currently also set in b9y.sh
redis_maxmemory = '256mb'
b9y_release = "0.36"
b9y_version = "0.36.1"

app = Bottle()

# The default path renders a hello world JSON message
@app.get('/')
def get_home():
	return(dict(msg="This is bambleweeny", release=str(b9y_release),\
	version=str(b9y_version), instance=cluster_id))

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

# Swagger
@app.get('/swagger')
def get_swagger():
	with open("/app/swagger.json", mode='r') as file_handle:
		file_content = file_handle.read()
	file_handle.close()
	sw = json.loads(file_content)
	return(dict(sw))

# Get Auth Token
@app.route('/auth/token', method='POST')
def get_token():
	# Get JSON Payload
	try:
		payload = json.load(request.body)
		username = payload["username"]
		password = payload["password"]
		pwhash = _get_password_hash(password)
	except:
		response.status = 400
		return dict({"message":"No valid JSON found in post body or mandatory fields missing."})

	user_list = rc.scan_iter("USER:*")
	for user in user_list:
		user_record = json.loads(rc.get(user))
		if user_record["username"] == username and user_record["hash"] == pwhash:
			user_token = _issue_token(user=username, id=user[5:], expiry=token_expiry_seconds)
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

# Backend Info
@app.route('/info', method='GET')
def backend_info():
	api_auth = _authenticate()

	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	i = {}
	i["redis_connection"] = {}
	i["redis_connection"]["host"] = redis_host
	i["redis_connection"]["port"] = redis_port
	i["redis_dbsize"] = rc.dbsize()
	i["redis_client_list"] = rc.client_list()
	i["redis_info"] = rc.info()

	return(i)

# Trigger Redis Save
@app.route('/save', method='GET')
def redis_save():
	api_auth = _authenticate()
	# Only Admin can do this
	if api_auth["admin"] != "True" or api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})
	rc.save()
	return(dict(info="ok"))

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
		username = payload["username"]
		password = payload["password"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	if _find_user(username) == "found":
		response.status = 400
		return dict({"info":"This user exists already."})

	# Set ID and password hash for user
	new_userid = rc.incr("_USERID_")
	pwhash = _get_password_hash(password)
	user_record = {}
	user_record["username"] = username
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
	user_out["username"] = user_record["username"]
	user_out["quota"] = user_record["quota"]

	return(dict(user_out))

# Set Quota for User
@app.route('/users/<id:int>', method='PUT')
def set_user_quota(id):
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
		user_out["username"] = user_record["username"]
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
	admin_record["hash"] = _get_password_hash(new_password)
	rc.set("USER:0", json.dumps(admin_record, ensure_ascii=False))

	return(dict(info="updated"))

# Read Key
@app.route('/keys/<id>', method='GET')
def get_key(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Does the key have a valid format?
	if _valid_identifier(str(id)) != True:
		response.status = 400
		return dict({"info":"Key format invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "KEY:"+str(user_id)+"::"+str(id)

	# Read from Redis
	try:
		key_content = rc.get(redis_key)
		if key_content == None:
			raise ValueError('not found')
	except:
		response.status = 404
		return dict({"info":"Not found."})

	response.content_type = 'text/plain'
	return(str(key_content))

# Increase Key
@app.route('/incr/<id>', method='GET')
def incr_key(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID and quota
	user_id = api_auth["id"]
	user_quota = _get_user_quota(user_id)
	current_number_of_resources = _user_resources_number(user_id)

 	# Does the key have a valid format?
	if _valid_identifier(str(id)) != True:
		response.status = 400
		return dict({"info":"Key name is invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "KEY:"+str(user_id)+"::"+str(id)

	# Does the key exist already?
	keyexists = rc.get(redis_key)
	if keyexists == None:
		if user_quota != 0 and current_number_of_resources >= user_quota:
			response.status = 400
			return dict({"info":"Quota exceeded."})

		# Increase the counter of resources for this user_record
		rc.incr("NUMRES:"+str(user_id))

	# Read from Redis
	try:
		key_content = rc.incr(redis_key)
	except:
		response.status = 400
		return dict({"info":"Error - key is probably not INT."})

	response.content_type = 'text/plain'
	return(str(key_content))

# Write Key
@app.route('/keys/<id>', method='PUT')
def write_key(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID and quota
	user_id = api_auth["id"]
	user_quota = _get_user_quota(user_id)
	current_number_of_resources = _user_resources_number(user_id)

	# Does the key have a valid format?
	if _valid_identifier(str(id)) != True:
		response.status = 400
		return dict({"info":"Key name is invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "KEY:"+str(user_id)+"::"+str(id)

	# Does the key exist already?
	keyexists = rc.get(redis_key)
	if keyexists == None:
		# Are we allowed to create more objects?
		if user_quota != 0 and current_number_of_resources >= user_quota:
			response.status = 400
			return dict({"info":"Quota exceeded."})

		# Increase the counter of resources for this user_record
		rc.incr("NUMRES:"+str(user_id))

	# Write to Redis
	try:
		rc.set(redis_key, request.body.read())
	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	return(dict(info="ok"))

# Delete Key
@app.route('/keys/<id>', method='DELETE')
def delete_key(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Does the key have a valid format?
	if _valid_identifier(str(id)) != True:
		response.status = 400
		return dict({"info":"Key name is invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "KEY:"+str(user_id)+"::"+str(id)

	# Does the key exist already?
	keyexists = rc.get(redis_key)
	if keyexists == None:
		response.status = 404
		return dict({"info":"Key not found."})

	# Delete from Redis
	try:
		rc.delete(redis_key)
		rc.decr("NUMRES:"+str(user_id))

	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	return(dict(info="ok"))

# List all Keys
@app.route('/keys', method='GET')
def get_all_keys():
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Construct Resource Location
	redis_key = "KEY:"+str(user_id)+"::*"

	# Resource Location is different for admin access
	# Since in that case we want all resources
	if api_auth["admin"] == "True":
		redis_key = "KEY:*"

	output = []
	keys_list = rc.scan_iter(redis_key)
	for res in keys_list:
		res_obj = {}
		details = _get_key_data(res)
		res_obj["key"] = details["id"]
		res_obj["owner"] = details["owner"]
		output.append(res_obj)

	return(dict(keys=output))

# List - Add Item
@app.route('/lists/<id>', method='POST')
def add_item_to_list(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID and quota
	user_id = api_auth["id"]
	user_quota = _get_user_quota(user_id)
	current_number_of_resources = _user_resources_number(user_id)

	# Does the key have a valid format?
	if _valid_identifier_lists(str(id)) != True:
		response.status = 400
		return dict({"info":"List name is invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "LIST:"+str(user_id)+"::"+str(id)

	# Does the list exist already?
	keyexists = rc.lrange(redis_key, 0, 0)
	if not keyexists:
		# Are we allowed to create more objects?
		if user_quota != 0 and current_number_of_resources >= user_quota:
			response.status = 400
			return dict({"info":"Quota exceeded."})

		# Increase the counter of resources for this user_record
		rc.incr("NUMRES:"+str(user_id))

	# Write to Redis
	try:
		rc.lpush(redis_key, request.body.read())
	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	return(dict(info="ok"))

# Lists - Get Item
@app.route('/lists/<id>', method='GET')
def get_list_item(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Does the key have a valid format?
	if _valid_identifier_lists(str(id)) != True:
		response.status = 400
		return dict({"info":"List name is invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "LIST:"+str(user_id)+"::"+str(id)

	# Read from Redis. If there's just one item left we need to
	# decrease NUMRES
	try:
		num_items = rc.llen(redis_key)
		if num_items == 1:
			rc.decr("NUMRES:"+str(user_id))
		key_content = rc.rpop(redis_key)
	except:
		response.status = 404
		return dict({"info":"Not found."})

	response.content_type = 'text/plain'
	return(str(key_content))

# Lists - Delete
@app.route('/lists/<id>', method='DELETE')
def delete_list(id):
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Does the key have a valid format?
	if _valid_identifier(str(id)) != True:
		response.status = 400
		return dict({"info":"Key name is invalid."})

	# Construct Resource Location from user_id and id
	redis_key = "LIST:"+str(user_id)+"::"+str(id)

	# Does the list exist already?
	keyexists = rc.lrange(redis_key, 0, -1)
	if not keyexists:
		response.status = 404
		return dict({"info":"List not found."})

	# Delete from Redis
	try:
		rc.delete(redis_key)
		rc.decr("NUMRES:"+str(user_id))

	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	return(dict(info="ok"))

# Lists - Get All
@app.route('/lists', method='GET')
def get_all_lists():
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	# Construct Resource Location
	redis_key = "LIST:"+str(user_id)+"::*"

	# Resource Location is different for admin access
	# Since in that case we want all resources
	if api_auth["admin"] == "True":
		redis_key = "LIST:*"

	output = []
	keys_list = rc.scan_iter(redis_key)
	for res in keys_list:

		res_obj = {}
		details = _get_key_data(res)
		res_obj["key"] = details["id"]
		res_obj["owner"] = details["owner"]
		output.append(res_obj)

	return(dict(lists=output))

# Create Route
@app.route('/routes', method='POST')
def create_route():
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]

	try:
		payload = json.load(request.body)

		key = payload["key"]
		content_type = payload["content_type"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	id = str(uuid.uuid4())

	# Construct Resource Location
	redis_key = "ROUTE:"+str(id)
	route_record = {}
	route_record["key"] = key
	route_record["content_type"] = content_type
	route_record["user_id"] = user_id

	# Write to Redis
	try:
		rc.set(redis_key, json.dumps(route_record, ensure_ascii=False))

	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	return(dict(info="ok", path="/routes/"+str(id)))

# Route - Read Key
@app.route('/routes/<id>', method='GET')
@app.route('/routes/<id>/<dummy>', method='GET')
@app.route('/routes/<id>/<dummy>/<dummy2>', method='GET')
@app.route('/routes/<id>', method='POST')
@app.route('/routes/<id>/<dummy>', method='POST')
@app.route('/routes/<id>/<dummy>/<dummy2>', method='POST')
def get_route(id, dummy=0, dummy2=0):
	route_key = "ROUTE:"+str(id)

	# Read Route from Redis
	try:
		route_content = rc.get(route_key)
		if route_content == None:
			raise ValueError('not found')

		route_record = json.loads(route_content)
		user_id = route_record["user_id"]
		key = route_record["key"]
		content_type = route_record["content_type"]

	except:
		response.status = 404
		return dict({"info":"Not found."})

	# Construct Resource Location from user_id and id
	redis_key = "KEY:"+str(user_id)+"::"+str(key)

	# Read from Redis
	try:
		key_content = rc.get(redis_key)
		if key_content == None:
			raise ValueError('not found.')
	except:
		response.status = 404
		return dict({"info":"Not found."})

	response.headers['Access-Control-Allow-Origin'] = '*'
	response.content_type = content_type
	return(parse_route(str(key_content), user_id))

# Create Bins
@app.route('/bins', method='POST')
def create_bin():
	api_auth = _authenticate()

	# Authorization is needed for this endpoint
	if api_auth["authenticated"] == "False":
		response.status = 401
		return dict({"info":"Unauthorized."})

	# Get User ID
	user_id = api_auth["id"]
	user_quota = _get_user_quota(user_id)
	current_number_of_resources = _user_resources_number(user_id)

	if user_quota != 0 and current_number_of_resources >= user_quota:
		response.status = 400
		return dict({"info":"Quota exceeded."})

	try:
		payload = json.load(request.body)

		list = payload["list"]
	except:
		response.status = 400
		return dict({"info":"No valid JSON found in post body or mandatory fields missing."})

	if _valid_identifier_lists(str(list)) != True:
		response.status = 400
		return dict({"info":"List name is invalid."})

	id = str(uuid.uuid4())

	# Construct Resource Location
	redis_key = "BIN:"+str(id)
	route_record = {}
	route_record["list"] = list
	route_record["user_id"] = user_id

	# Write to Redis
	try:
		rc.set(redis_key, json.dumps(route_record, ensure_ascii=False))
	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	# Increase the counter of resources for this user_record
	rc.incr("NUMRES:"+str(user_id))

	return(dict(info="ok", path="/bins/"+str(id)))

# Post to Bin
@app.route('/bins/<id>', method='POST')
def post_to_bin(id):
	bin_key = "BIN:"+str(id)

	# Read Bin from Redis
	try:
		bin_content = rc.get(bin_key)
		if bin_content == None:
			raise ValueError('not found')

		bin_record = json.loads(bin_content)
		user_id = bin_record["user_id"]
		list = bin_record["list"]

	except:
		response.status = 404
		return dict({"info":"Not found."})

	# Construct Resource Location from user_id and id
	redis_key = "LIST:"+str(user_id)+"::"+str(list)

	try:
		rc.lpush(redis_key, request.body.read())
	except:
		response.status = 400
		return dict({"info":"not a valid request"})

	return("OK")

####### Helper functions
# Parse Routes for nested keys
def parse_route(content, user_id):
	if re.search('!@\[[_a-zA-Z0-9:]*\]', content):
		response.headers["B9Y-ROUTES"] = "parsed"
		repl1 = re.sub('!@\[[_a-zA-Z0-9:]*\]', '_B9yPrsE_\\g<0>_B9yPrsE_', content)
		items = repl1.split("_B9yPrsE_")
		out = ""
		for i in items:
			if i.startswith("!@["):
				key = re.sub('[^\w:]', "", i)
				val = rc.get("KEY:"+str(user_id)+"::"+str(key))
				if val != None:
					out += val
			else:
				out += str(i)
		return(out)
	else:
		return(content)

# Key names must match this regex
def _valid_identifier(i):
	return(re.match("[_A-Za-z:][_a-zA-Z0-9:]*$", i) and not keyword.iskeyword(i))

# List names must match this regex
def _valid_identifier_lists(i):
	return(re.match("[_A-Za-z][_a-zA-Z0-9]*$", i) and not keyword.iskeyword(i))

def _get_key_data(k):
	out = {}
	pos = k.find("::")
	pos1 = k.find(":")
	out["id"] = k[pos+2:]
	out["owner"] = k[pos1+1:pos]
	return(out)

def _get_password_hash(pw):
	hash_object = hashlib.sha1(pw+salt)
	return(hash_object.hexdigest())

def _create_admin():
	pwhash = _get_password_hash(admin_password)
	user_record = {}
	user_record["username"] = "admin"
	user_record["hash"] = pwhash
	user_record["quota"] = "0"

	rc.set("USER:0", json.dumps(user_record, ensure_ascii=False))

	return

def _find_user(username):
    user_list = rc.scan_iter("USER:*")
    for user in user_list:
        user_record = json.loads(rc.get(user))
        if user_record["username"] == username:
            return("found")

    return("not found")

def _get_user_quota(uid):
	user_record = json.loads(rc.get("USER:"+str(uid)))

	return int(user_record["quota"])

def _user_resources_number(uid):
	n = rc.get("NUMRES:"+str(uid))
	if n == None:
		return 0
	else:
		return(int(n))

def _b64_enc(s):
	return(base64.urlsafe_b64encode(s))

def _b64_dec(s):
	return(base64.urlsafe_b64decode(s))

def _issue_token(user, expiry, id):
	# Dict containing user info
	content = {}
	content["u"] = user
	content["t"] = str(int(time.time()))
	content["i"] = id
	content["c"] = str(cluster_id)

	# Create base64 encoded version
	c = _b64_enc(json.dumps(content))

	# Get an hmac signature
	hmac1 = hmac.new(salt, c, hashlib.sha256)

	return(c + "." + hmac1.hexdigest()[:8])

def _get_token_data(token):
    token_data = {}
    token_data["error"] = "0"
    token_data["admin"] = "False"
    token_data["authenticated"] = "False"

    try:
        # Get base64 encoded content and the signature from the token
        separator = token.find(".")
        sig_token = token[separator+1:]
        content_raw = _b64_dec(token[:separator])
        content = json.loads(content_raw)

        # Create signature
        c = base64.urlsafe_b64encode(json.dumps(content))
        hmac1 = hmac.new(salt, c, hashlib.sha256 )
        sig_check = hmac1.hexdigest()[:8]

        # Only get the data if the signature is valid
        if sig_token == sig_check:
            token_data["timestamp"] = int(content["t"])
            token_data["user"] = content["u"]
            token_data["id"] = content["i"]
            token_data["cluster_id"] = content["c"]

            if content["u"] == 'admin':
                token_data["admin"] = "True"
        else:
            token_data["error"] = "1"
    except:
        token_data["error"] = "1"

    return(token_data)

def _authenticate():
	# Token can be in query string or AUTH header
	if 'token' in request.query:
		access_token = request.query["token"]
	else:
		bearer = request.environ.get('HTTP_AUTHORIZATION','')
		access_token=bearer[7:]

	# Extract the data from the token
	data = _get_token_data(token=access_token)

	# If there was an error, end here
	if data["error"] != "0":
		return(dict(data))

	# Was the token issued by this cluster?
	if data["cluster_id"] != cluster_id:
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

def _cluster_init():
	cid = str(uuid.uuid4())
	rc.set("_B9Y_ID_", cid[:8])
	rc.set("__SALT__", salt)

	return(cid[:8])

def queue_housekeeping():
	rc.set("_LASTRUN_", str(int(time.time())))

def processor():
    while True:
        time.sleep(60)
        queue_housekeeping()

# Initialization
# We need a Redis connection
if not "redis_host" in os.environ or not "redis_port" in os.environ:
	exit("ERROR: please set the environment variables for Redis host")

# Connect to the Redis backend
redis_host = os.environ['redis_host']
redis_port = os.environ['redis_port']

if "redis_password" in os.environ:
	redis_password = os.environ['redis_password']
else:
	redis_password = ""

rc = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, db=0)

# Configure local Redis
if "redis_embedded" in os.environ:
	rc.config_set('dir', redis_datadir)
	rc.config_set('maxmemory', redis_maxmemory)

# Set Token expiry
if 'token_expiry' in os.environ:
	token_expiry_seconds = int(os.environ['token_expiry'])
else:
	token_expiry_seconds = default_token_expiry_seconds

# Set Salt
if 'salt' in os.environ:
	salt = os.environ['salt']
else:
	salt = default_salt

# Create record for admin user if it doesn't exist
try:
	if rc.get("USER:0") == None:
		_create_admin()
except:
	print "ERROR: Unable to connect to Redis at " + str(redis_host) + ":" + redis_port
	exit(1)

# Read unique ID for this instance / cluster or initialize if it doesn't exist
cluster_id = rc.get("_B9Y_ID_")

if cluster_id == None:
	cluster_id = _cluster_init()

multiproc = Process(target=processor)
multiproc.start()
