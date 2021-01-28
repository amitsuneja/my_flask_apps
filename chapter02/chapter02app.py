from flask import Flask
from flask import request
from flask import render_template
#from flask import make_response
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename


import json
import os

app = Flask(__name__)


@app.route('/register/')
def register():
	return render_template('register.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		return render_template("result.html",result = result)


@app.route('/')
def index():
   return render_template('upload.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully : ' + f.filename



if __name__ == '__main__':
	# Set the secret key to some random bytes. Keep this really secret!
	app.secret_key = os.urandom(16)
	app.config['SESSION_TYPE'] = 'filesystem'
       
	app.run(host= '0.0.0.0',debug=True,port=5000)
