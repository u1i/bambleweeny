from bottle import Bottle, request, view, response
from bwy_functions import issue_token, get_token_data
import json, os, uuid, base64, redis, time, hashlib

# Settings
admin_password = u"changeme"
secret_salt = "iKm4SyH6JCtA8l"
token_expiry_seconds = 300

app = Bottle()

# The default path renders a hello world JSON message
@app.get('/')
def get_home():
	return(dict(msg="This is bambleweeny."))

# Not found
@app.error(404)
def error404(error):
    #return 'Nothing here, sorry'
	return("Nothing here.")

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
		admin_token = issue_token(user=username, expiry=token_expiry_seconds)
		return(dict(token_type="bearer", access_token=admin_token))

	# Normal User
	user_list = rc.scan_iter("USER:*")
	for user in user_list:
		user_record = json.loads(rc.get(user))
		if user_record["email"] == username and user_record["hash"] == pwhash:
			admin_token = issue_token(user=username, expiry=token_expiry_seconds)
			return(dict(token_type="bearer", access_token=admin_token))

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

# Helper functions

def _authenticate():
	bearer = request.environ.get('HTTP_AUTHORIZATION','')
	access_token=bearer[7:]

	# Extract the data from the token
	data = get_token_data(access_token)

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
