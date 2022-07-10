from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///PriceTracker.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

numMax = 3

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100),nullable=False)
	email = db.Column(db.String(50),nullable=False)
	password = db.Column(db.String(50),nullable=False)
	urlString = db.Column(db.String(2000))
	priceString = db.Column(db.String(700))
	dateString = db.Column(db.String(2000))
	num = db.Column(db.Integer)

def __repr__(self):
		return '<Name %r>' % self.id


#scraaping
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def flipkartPrice(aUrl):
    response = requests.get(aUrl,headers = headers)
    doc = BeautifulSoup(response.text,'html.parser')
    price = doc.find_all('div',{'class':'_30jeq3 _16Jk6d'})
    if price == []:
        return (-1)
    else:
        return(price[0].text.strip())
#ends

@app.route('/signup',methods=["GET","POST"])
def signup():
	if request.method == "POST":
		Name = request.form.get("name")
		Email = request.form.get("email_name")
		Password1 = request.form.get("password1")
		Password2 = request.form.get("password2")
		error_1 = ""
		if not Name or not  Email or not Password1 or not Password2:
			error_1="All fields need to be filled"
			return render_template("signup.html",Password1=Password1,Password2=Password2,error_1=error_1,Name=Name,Email=Email)

		if Password1 != Password2:
			error_1="Password is not matching"
			return render_template("signup.html",Password1=Password1,Password2=Password2,error_1=error_1,Name=Name,Email=Email)

		flag = User.query.filter_by(email = Email).first()
		if flag:
			error_1="This email is already registered"
			return render_template("signup.html",Password1=Password1,Password2=Password2,error_1=error_1,Name=Name,Email=Email)
		new_name = Name
		stdt=User(name=new_name,email=Email,password=Password1)

		try:
			db.session.add(stdt)
			db.session.commit()
		except:
			return "error 404"

		return render_template("login.html")
	else:
		error_1 = ""
		return render_template("signup.html")

@app.route('/',methods=["POST","GET"])
def login():
	if request.method == "POST":
		Email = request.form.get("email_name")
		Password = request.form.get("password")
		error_1 = ""
		if not Email or not Password:
			error_1="All fields need to be filled"
			return render_template("login.html",error_1=error_1,Password=Password,Email=Email)
		flag = User.query.filter_by(email = Email).first()
		if not flag:
			error_1="Email doesn't exist"
			return render_template("login.html",error_1=error_1,Password=Password,Email=Email)
		if flag.password != Password:
			error_1="Password doesn't match"
			return render_template("login.html",error_1=error_1,Password=Password,Email=Email)
		return render_template("inter.html",email = Email)
	else:
		error_1 = ""
		return render_template("login.html")

@app.route('/home/<email>')
def home(email):
	global numMax
	return render_template("home.html",email=email,numMax=numMax)

@app.route('/add/<email>',methods=["POST","GET"])
def add(email):
	global numMax
	if request.method == "POST":
		price = request.form.get("name")
		url = request.form.get("urlname")
		zz = flipkartPrice(url)
		if zz==(-1):
			error_1 = "Either the URL is invalid or we are unable to track the product"
			return render_template("add.html",email=email,error_1=error_1)
		flag = User.query.filter_by(email = email).first()
		if not flag.priceString:
			flag.priceString = ""
			flag.urlString = ""
			flag.dateString = ""
			flag.num = 0
		flag.priceString += str(price)+str('#')
		flag.urlString += url + str('#')
		date_time = datetime.today()
		zz= str(date_time)[:10]
		zz += '#'
		flag.dateString += str(zz)
		flag.num += 1
		db.session.commit()
		return render_template("inter.html",email=email)
	else:
		flag = User.query.filter_by(email = email).first()
		if flag.priceString:
			if flag.num == numMax :
				mess1 = " sorry U have exhausted all your chances, first delete some Urls to add more "
				return render_template("inter2.html",mess1=mess1,email=email)
		return render_template("add.html",email=email)

@app.route('/mylist/<email>')
def mylist(email):
	flag = User.query.filter_by(email = email).first()
	a1 = []
	a2 = []
	a3 = []
	a4 = []
	if not flag.priceString or flag.num == 0:
		return render_template("mylist.html",a1=a1,a2=a2,a3=a3,a4=a4,email = email)
	i = 0
	j = 0
	k = 0
	S1 = flag.priceString
	S2 = flag.urlString
	S3 = flag.dateString
	while i<len(S1) :
		s1 = ""
		s2 = ""
		s3 = ""
		while S1[i] != '#' :
			s1 += S1[i]
			i += 1
		while S2[j] != '#' :
			s2 += S2[j]
			j += 1
		while S3[k] != '#' :
			s3 += S3[k]
			k += 1
		zz = flipkartPrice(s2)
		a1.append(s1)
		a2.append(s2)
		a3.append(s3)
		a4.append(zz)
		i += 1
		j += 1
		k += 1
	return render_template("mylist.html",a1=a1,a2=a2,a3=a3,a4=a4,email = email)

@app.route('/cancel/<email>/<int:id>')
def cancel(email,id):
	i = 0
	j = 0
	k = 0
	z = 0
	sf1 = ""
	sf2 = ""
	sf3 = ""
	flag = User.query.filter_by(email = email).first()
	S1 = flag.priceString
	S2 = flag.urlString
	S3 = flag.dateString
	while i<len(S1) :
		s1 = ""
		s2 = ""
		s3 = ""
		while S1[i] != '#' :
			s1 += S1[i]
			i += 1
		while S2[j] != '#' :
			s2 += S2[j]
			j += 1
		while S3[k] != '#' :
			s3 += S3[k]
			k += 1

		if z != id:
			sf1 += s1 + '#'
			sf2 += s2 + '#'
			sf3 += s3 + '#'
		z += 1
		i += 1
		j += 1
		k += 1
	flag.priceString = sf1
	flag.urlString = sf2
	flag.dateString = sf3
	flag.num -= 1
	db.session.commit()
	return render_template("inter.html",email = email)

app.run(debug=True)