# Getting Started with Bambleweeny

## Run with Docker

You'll quickly get a simple, self-contained version running with the following command:

`docker run -d -p 8080:8080 u1ih/bambleweeny`

Assuming you have Docker and docker-compose installed on your machine, you could also do this a little better and deploy a topology instead:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

## Admin Access

Bambleweeny should now be available at `http://localhost:8080` - however, there's not much to see. It's all about the API. We'll use cURL examples here.

To access with the key/value store we need to make authenticated requests, so as a first step we are getting an access token. For this, we login with username and password.

### Create a new user

The default password for 'admin' is 'changeme', let's get a token so we can access the API:

`curl -X POST "http://localhost:8080/auth/token?raw" -H 'Content-Type: application/json' -d '{ "username": "admin", "password": "changeme"}'`

> eyJpIjogIjAiLCAiYyI6ICI4MjgxNWU4NiIsICJ1IjogImFkbWluIiwgInQiOiAiMTUzODI3MjYxOCJ9.57f8e251

We've received a token (copy it and replace `TOKEN` in the following cURL command), which we can now use to make an authenticated request (as admin) and create a new user with email address (username) 'me@privacy.net' and password 'changeme':

`curl -X POST http://localhost:8080/users -H "Authorization: Bearer TOKEN" -H 'Content-Type: application/json' -d '{ "email": "me@privacy.net", "password": "changeme" }'`

> {"info": "created", "id": 1}

## Create and Access Keys

Now we have a user account and can create and access keys and resources.

### Write a key
Let's create a key! First, we need to login with that new user:

`curl -X POST "http://localhost:8080/auth/token?raw" -H 'Content-Type: application/json' -d '{ "username": "me@privacy.net", "password": "changeme"}'`

Copy the output again and replace `TOKEN` in the following command with the token we received.

`echo $RANDOM | curl -X PUT -d @- http://localhost:8080/keys/mykey1 -H "Authorization: Bearer TOKEN"`

### Get a key

That was easy, right? You can now read the key with:

`curl http://localhost:8080/keys/mykey1 -H "Authorization: Bearer TOKEN"`

That's it! Check out the full API documentation for key, quota & identity management requests.

## Increment Keys

Looking for a way to implement a counter, or hand out queue / ticket numbers? It's easy with Bambleweeny!

`curl http://b9y/incr/queue_number -H "Authorization: Bearer TOKEN"`

Issue this request a couple of times, and the output will increase by 1 each time. Even if you run B9Y in cluster mode, there'll be no overlap.



