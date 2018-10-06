from b9y import B9y

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
