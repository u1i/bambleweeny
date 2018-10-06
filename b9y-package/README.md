![](https://raw.githubusercontent.com/u1i/bambleweeny/master/img/bwy2.png)

# b9y - Python Bindings for Bambleweeny

A client implementation for [Bamblweeny](https://github.com/u1i/bambleweeny)

## Install
pip install b9y


## Use

from b9y import B9y

b9y = B9y() # for default connection

b9y = B9y('http://myhost:8080')

b9y = B9y('http://myhost:8080', 'user', 'password')

#### Get info
print b9y.info()

#### Set and get key
b9y.set('foo', 'bar')   
print b9y.get('foo')

#### Try the counter
print b9y.incr('counter')

#### Push and pop
b9y.push('super', 'trouper')
print b9y.pop('super')

## PyPi

[b9y-cli on pypi](https://pypi.org/project/b9y/)
