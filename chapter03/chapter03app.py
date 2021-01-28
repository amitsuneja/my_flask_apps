from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask_bootstrap import Bootstrap
from flask import session
from werkzeug import secure_filename


import json
import os

app = Flask(__name__)


@app.route('/cookiesindexpage')
def indexPageofcookies():
   return render_template('loginWithCookies.html')

@app.route('/saveCookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
       resp = make_response(render_template('result.html'))
       resp.headers['Access-Control-Allow-Origin'] = '*'	
       resp.set_cookie('user', request.form['user'])       
       return resp

@app.route('/dashboardOfCookie')
def dashboardForCookie():
   name = request.cookies.get('user')
   return 'Hello ' + name 

"""
Cookies and Sessions: They are used to store information. Cookies are only stored on the client-side machine, while 
sessions get stored on the client as well as a server.

Session
-------
A session creates a file in a temporary directory on the server where registered session variables and their values 
are stored. This data will be available to all pages on the site during that visit.
A session ends when the user closes the browser or after leaving the site, the server will terminate the session after 
a predetermined period of time, commonly 30 minutes duration.

Cookies
-------
Cookies are text files stored on the client computer and they are kept of use tracking purpose. Server script sends a 
set of cookies to the browser. For example name, age, or identification number etc. The browser stores this information
on a local machine for future use.
When next time browser sends any request to web server then it sends those cookies information to the server and server uses that information to identify the user.
Note: We are creating example of both session and cookies , but cookies has no logout route
"""


@app.route('/sessionindexpage')
def indexPageofSession():
   return render_template('loginWithSession.html')

@app.route('/saveSession', methods = ['POST', 'GET'])
def setSession():
   if request.method == 'POST':
       session['user'] = request.form['user']
       resp = make_response(render_template('result.html'))
       
       return resp

@app.route('/dashboardOfSession')
def dashboardForSession():
   name = session['user']
   return 'Hello ' + name 

@app.route('/logout')
def deleteSession():
    session.pop('user', None)
    return ''


if __name__ == '__main__':
	# Set the secret key to some random bytes. Keep this really secret!
	app.secret_key = os.urandom(16) # delete this line for cookies
	app.config['SESSION_TYPE'] = 'filesystem'  # delete this line for cookies
       
	app.run(host= '0.0.0.0',debug=True,port=5000)
