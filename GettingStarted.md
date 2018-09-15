# Getting Started with Bambleweeny

## Run with Docker

Assuming you have Docker and docker-compose installed on your machine, the following command pulls and runs Bambleweeny for you:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

## Admin Access

Bambleweeny should now be available at `http://localhost:8080` - however, there's not much to see. It's all about the API. We'll use cURL examples here.

To work with resources we need to make authenticated requests, so as a first step we are getting an access token. For this, we login with username and password.

### Create a new user

The default password for 'admin' is 'changeme', let's get a token so we can access the API:

`curl -X POST "http://localhost:8080/auth/token?raw" -H 'Content-Type: application/json' -d '{ "username": "admin", "password": "changeme"}'`

> eyJpIjogMCwgInUiOiAiYWRtaW4iLCAidCI6ICIxNTM3MDA0NzcwIn0=.576f5f00df3b6e5ac8430df435f0f6e586a57e3dddc3f26b1e5fc19535543092

We've received a token, which we can now use to make an authenticated request (as admin) and create a new user with email address (username) 'me@privacy.net' and password 'changeme':

`curl -X POST http://localhost:8080/users -H "Authorization: Bearer $token" -H 'Content-Type: application/json' -d '{ "email": "me@privacy.net", "password": "changeme" }'`

> {"info": "created", "id": 1}

## Create a Resource as a User

Now we have a user account and can create resources (admin can have resources as well, but why would you do such a thing?):

`curl -X POST http://localhost:8080/resources -H "Authorization: Bearer $token" -H 'Content-Type: application/json' -d '{ "content": "lorem ipsum" }'`

> {"info": "created", "id": "145a6f04-6775-4479-9832-e082f91ae7dd"}

That's it! Check out the full API documentation for read, delete, and quota & identity management requests.


