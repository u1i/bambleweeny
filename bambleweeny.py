from bottle import Bottle, request, view, response
from bwy_functions import issue_token, get_token_data
import json, os, uuid, base64, redis, time, hashlib

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
		hash_object = hashlib.sha1(password)
		pwhash = hash_object.hexdigest()
	except:
		response.status = 400
		return dict({"message":"No valid JSON found in post body or mandatory fields missing."})

	# ADMIN access
	if username == 'admin' and password == admin_password:
		admin_token = issue_token(user=username, id=0, expiry=token_expiry_seconds, salt=secret_salt)

		if 'raw' in request.query:
			return(admin_token)
		else:
			return(dict(token_type="bearer", access_token=admin_token))

	# Normal User
	user_list = rc.scan_iter("USER:*")
	for user in user_list:
		user_record = json.loads(rc.get(user))
		if user_record["email"] == username and user_record["hash"] == pwhash:
			user_token = issue_token(user=username, id=user[5:], expiry=token_expiry_seconds, salt=secret_salt)
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

	# Set ID and password hash for user
	new_userid = rc.incr("_USERID_")
	hash_object = hashlib.sha1(password)
	pwhash = hash_object.hexdigest()

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

	# Does the user exist?
	if rc.get("USER:"+str(id)) == None:
		response.status = 404
		return dict({"info":"Not found."})

	# Delete user resources
	# TBD

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

	return(dict(output=output))




####### Helper functions

def _authenticate():
	bearer = request.environ.get('HTTP_AUTHORIZATION','')
	access_token=bearer[7:]

	# Extract the data from the token
	data = get_token_data(token=access_token, salt=secret_salt)

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
		user_record = {}
		user_record["email"] = "admin@admin"
		user_record["hash"] = "nil"
		user_record["quota"] = "0"

		rc.set("USER:0", json.dumps(user_record, ensure_ascii=False))
