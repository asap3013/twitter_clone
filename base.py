from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import flask_login
import MySQLdb.cursors
from flask_login import LoginManager
from flask import json , jsonify
from json import JSONEncoder
import yaml
import json


app = Flask(__name__)
dbs= yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = dbs['mysql_host']
app.config['MYSQL_USER'] = dbs['mysql_user']
app.config['MYSQL_PASSWORD'] = dbs['mysql_password']
app.config['MYSQL_DB'] = dbs['mysql_db']
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
db = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class User(flask_login.UserMixin):
    def get_id(self):
        return self.get_id
    pass
@property
def is_active(self):
 	return False

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


#Login page
@app.route('/',methods=['GET','POST'])
def login_page():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = %s AND password = %s', (email, password))
        User = cursor.fetchone()
        if User:
            email = User['email']
            password= User['password']
            return redirect('/home_page')        
        else:
            msg = 'Incorrect username / password !'
    return render_template('login_form.html')


#Register Page
@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method =='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cur = db.connection.cursor()
        
        cur.execute('INSERT INTO User(first_name,last_name,username,email,password) VALUES(%s,%s,%s,%s,%s)',(first_name,last_name,username,email,password))

        db.connection.commit()
        cur.close()
        return render_template('login_form.html')
    return render_template('register_form.html') 

#Main Page
@app.route('/home_page',methods = ['GET','POST'])
def home_page():
    return render_template('home.html')

class MyEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__   

@login_manager.user_loader
@app.route('/tweets',methods = ['GET','POST'])
def tweets():
    if request.method == 'POST':
        breakpoint()
        user = User()
        user_id = json.dumps(user,cls=MyEncoder)
        uid = flask_login.login_user(id)
        content = request.form['content']
        data = [{'name':uid,'content':content}]
        cur = db.connection.cursor()
        cur.execute('INSERT INTO Tweets(uid,content) VALUES(%s,%s)',(uid,content))
        db.connection.commit()
        cur.close()
        return jsonify(data) 
    else:
        return 'wrong info'


if __name__ == "__main__":
    app.run(debug=True,port=7000)