from flask import Flask
from flask import request
from flask import abort
from flask import render_template
from flask import send_file
from flask import flash
from flask import url_for
from flask import redirect
#from flask import make_response
#from flask import session
from flask_bootstrap import Bootstrap

import json
import os

app = Flask(__name__)


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
        base_dir = '/root/my_flask_apps/chapter01'
        print("base_dir = ",base_dir)

        # Joining the base and the requested path
        abs_path = os.path.join(base_dir, req_path)
        print("abs_path = ",abs_path)

        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
                print(abs_path + " not find at OS lvel using os.path.exists")
                return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
                print(abs_path + " is file and i am serving it")
                return send_file(abs_path)

        # Show directory contents
        print(abs_path + " is a directory so i am listing files using template")
        files = os.listdir(abs_path)
        return render_template('firstAppTemplate.html', files=files)


@app.route('/learningflask')
def index():
        hello_dict = dict()
        hello_dict["custom.keys"] = "auto contents of your http request"
        hello_dict["request.url"] = request.url
        hello_dict["request.base_url"] = request.base_url
        hello_dict["request.url_charset"] = request.url_charset
        hello_dict["request.url_root"] = request.url_root
        hello_dict["request.host_url"] = request.host_url
        hello_dict["request.host"] = request.host
        hello_dict["request.script_root"] = request.script_root
        hello_dict["request.path"] = request.path
        hello_dict["request.full_path"] = request.full_path
        hello_dict["request.args"] = request.args
        hello_dict["request.url_rule"] = str(request.url_rule)
        return json.dumps(hello_dict)


@app.route('/hello/<nameasVar>')
def sayhello(nameasVar):
    return "Helllo hello " + nameasVar


@app.route('/hello/<string:nameasVar>/<string:ageAsVar>')
def person(nameasVar,ageAsVar):
    return nameasVar + "  your age is:" + ageAsVar

#Templates are stored in the /templates/ directory
#A template is an HTML file (Flask uses the Jinja template engine)
#Templates can contain Python variables using this syntax {{x}}
@app.route('/howtopassvartotemplate/<name>')
def justForOneVar(name):
    return render_template("hello.html",name=name)


#An URL route can have more than one variables
#To pass multiple variables to a template, create dictionary and pass it to template
#Inside template - iterate over the dictionary
# You can also create List and pass it as variable to template
@app.route('/howtopassmultivartotemplate/<value1>/<value2>/<value3>')
def justForMultiVar(value1,value2,value3):
    myDict = {'Key1':value1, 'Key2':value2,'Key3':value3} 
    return render_template("helloWithMyDictTemplate.html", myDict=myDict) 

#Static files (images, downloadables) are stored in the /static/  folder
# Load a static file like this {{ url_for('static', filename = 'city.jpg') }}



#BMI calculator (Formula = BMI = weight / (length*length)

@app.route('/printBmi/<bmi>')
def printBmiOfUser(bmi):
   return 'Your BMI is %s' % str(bmi)

@app.route('/bmi',methods = ['POST', 'GET'])
def bmiCalculator():
   if request.method == 'POST':
      height = request.form['height']
      height = float(height)
      mass = request.form['mass']      
      mass = float(mass)
      bmi = mass / (height*height)
      bmi = round(bmi,2)
      return redirect(url_for('printBmiOfUser',bmi=bmi))
   if request.method == 'GET':
      return render_template('bmiCalculatorTemplate.html')


@app.route('/success/<name>')
def success(name):
      return 'welcome %s' % name

@app.route('/loginTemp',methods = ['POST', 'GET'])
def login_temp():
   if request.method == 'POST':
      user = request.form['username']
      return redirect(url_for('success',name = user))
   if request.method == 'GET':
      return render_template('loginTempFirstTemplate.html')




# '/login' wont work , so make sure yopu write '/login/'
@app.route('/login/', methods=["GET", "POST"])
def login_page():
        """
        For GET requests, display the login form.
        For POSTS, login the current user by processing the form.
        """
        error = ''
        tpass = False

        try:
                if request.method == "POST":

                        attempted_username = request.form['username']
                        attempted_password = request.form['password']
			# https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/#message-flashing-pattern
                        flash(attempted_username)
                        flash(attempted_password)

                        if attempted_username == "admin" and attempted_password == "password":
                                tpass = True

                        else:
                                tpass = False
                                error = "Invalid credentials. Try Again."

                if tpass:
                        return redirect(url_for('dir_listing'))
                else:
                        return render_template("loginPageTemplate.html", error=error)

        except Exception as e:
                flash(e)
                return render_template("loginPageTemplate.html", error=error)



if __name__ == '__main__':
	# Set the secret key to some random bytes. Keep this really secret!
	app.secret_key = os.urandom(16)
	app.config['SESSION_TYPE'] = 'filesystem'
       
	app.run(host= '0.0.0.0',debug=True,port=5000)
