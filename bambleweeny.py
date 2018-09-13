from bottle import Bottle, request, view

app = Bottle()

@app.get('/')
def get_home():

	return("hello!")

@app.get('/api')
def do_api():

	return(dict(msg="hello!"))

@app.get('/template')
@view('my')
def do_templ():
	return(dict(message="hello!"))
