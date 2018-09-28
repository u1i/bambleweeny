# Getting Started with Bambleweeny

## Run with Docker

You'll quickly get a simple, self-contained version running with the following command:

`docker run -d -p 8080:8080 u1ih/bambleweeny`

Assuming you have Docker and docker-compose installed on your machine, you could also do this a little better and deploy a topology instead:

`curl -sSL http://bit.ly/run-bambleweeny | sh`

## Admin Access

Bambleweeny should now be available at `http://localhost:8080` - however, there's not much to see. It's all about the API. We'll use cURL examples here.

To work with resources we need to make authenticated requests, so as a first step we are getting an access token. For this, we login with username and password.

### Create a new user

The default password for 'admin' is 'changeme', let's get a token so we can access the API:

`curl -X POST "http://localhost:8080/auth/token?raw" -H 'Content-Type: application/json' -d '{ "username": "admin", "password": "changeme"}'`

> eyJpIjogMCwgInUiOiAiYWRtaW4iLCAidCI6ICIxNTM3MDA0NzcwIn0=.576f5f00df3b6e5ac8430df435f0f6e586a57e3dddc3f26b1e5fc19535543092

We've received a token (copy it and replace `TOKEN` in the following cURL command), which we can now use to make an authenticated request (as admin) and create a new user with email address (username) 'me@privacy.net' and password 'changeme':

`curl -X POST http://localhost:8080/users -H "Authorization: Bearer TOKEN" -H 'Content-Type: application/json' -d '{ "email": "me@privacy.net", "password": "changeme" }'`

> {"info": "created", "id": 1}

## Create a Resource as a User

Now we have a user account and can create resources (admin can have resources as well, but why would you do such a thing?):

So first, we need to login with that new user:

`curl -X POST "http://localhost:8080/auth/token?raw" -H 'Content-Type: application/json' -d '{ "username": "me@privacy.net", "password": "changeme"}'`

Copy the output again and replace `TOKEN` in the following command with the token we received. Because now we're creating our first resource, with `lorem ipsum` as a content.

`curl -X POST http://localhost:8080/resources -H "Authorization: Bearer TOKEN" -H 'Content-Type: application/json' -d '{ "content": "lorem ipsum" }'`

> {"info": "created", "id": "145a6f04-6775-4479-9832-e082f91ae7dd"}

We receive the unique ID of the newly created resource which we can use to access it with a GET request on the object.

That's it! Check out the full API documentation for read, delete, and quota & identity management requests.


