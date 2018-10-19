from bindings import B9y
import random

b9y = B9y()

# Get info
print b9y.info()

# Set and get key
b9y.set('foo', 'bar')
print b9y.get('foo')

# Try the counter
print b9y.incr('counter')
print b9y.incr('counter')
print b9y.incr('counter')

# Push and pop
b9y.push('super', 'trouper')
print b9y.pop('super')

# Create Route
print(b9y.create_route('bla','text/html'))

# Create User
print(b9y.create_user('user'+str(random.randint(100,999)),'secret'))

# List Users
users = b9y.list_users()

print("Token: " + b9y.get_token())

print(users["users"])

# Trigger save on Redis
b9y.save()

# Set admin password
b9y.set_admin_password("bla")
