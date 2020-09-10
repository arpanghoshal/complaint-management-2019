import requests
from flask import Flask, render_template, request,Flask,request,jsonify,render_template, redirect, url_for,flash,session,abort
from flask_sqlalchemy import SQLAlchemy 
import smtplib
import psycopg2
from flask_bootstrap import Bootstrap
import os
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
UPLOAD_FOLDER = '/home/arpan/Desktop/'
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

class user(db.Model):
	__tablename__ = "user"
	id = db.Column('user_id',db.Integer , primary_key=True)
	username = db.Column('username', db.String(20), unique=True , index=True)
	password = db.Column('password' , db.String(10))
	email = db.Column('email',db.String(50),unique=True , index=True)
 
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
@app.before_first_request
def create_tables():

    db.create_all()


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
hostname = 'localhost'
username = 'postgres'
password = '********'
database = 'trial'
syd1=""
stud=""

labels=['ASSIGNED','CLOSED','OPEN']

@app.route("/client")
def uploadq():

	return render_template('hiii.html')

@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("uploadwwl"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		uname = request.form['uname']
		mail = request.form['mail']
		passw = request.form['passw']

		register = user(username = uname, email = mail, password = passw)
		db.session.add(register)
		db.session.commit()

		return redirect(url_for("login"))

	return render_template('register.html')


@app.route("/home")
def uploadww():

	return render_template('home.html')

@app.route("/homel")
def uploadwwl():
	myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
	myConnection.autocommit = True
	cur = myConnection.cursor()
	susu=""
	cur.execute("SELECT COUNT(*) FROM persons WHERE status='OPEN' UNION SELECT COUNT(*) FROM persons WHERE status='ASSIGNED' UNION SELECT COUNT(*) FROM persons WHERE status='RESOLVED';")

	baroo = cur.fetchall()
	baroo = str(baroo)
	baroo= baroo.replace(',','')
	baroo= baroo.replace('(','')
	baroo= baroo.replace(')','')
	baroo= baroo.replace('[','')
	baroo= baroo.replace(']','')
	baroo = [x.strip() for x in baroo.split(' ')]
	print(baroo)

	myConnection.close()


	return render_template('homeq.html', max=100, labels=labels, values=baroo)


@app.route('/bar')
def bar():
	
	



	myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
	myConnection.autocommit = True
	cur = myConnection.cursor()
	susu=""
	cur.execute("SELECT COUNT(*) FROM persons WHERE status='OPEN' UNION SELECT COUNT(*) FROM persons WHERE status='ASSIGNED' UNION SELECT COUNT(*) FROM persons WHERE status='RESOLVED';")

	baroo = cur.fetchall()
	baroo = str(baroo)
	baroo= baroo.replace(',','')
	baroo= baroo.replace('(','')
	baroo= baroo.replace(')','')
	baroo= baroo.replace('[','')
	baroo= baroo.replace(']','')
	baroo = [x.strip() for x in baroo.split(' ')]
	print(baroo)

	myConnection.close()



	return render_template('bar.html', max=100, labels=labels, values=baroo)



@app.route('/emailkro', methods=['GET', 'POST'])
def mailkro():
	if request.method == 'POST':
		emailid = request.form['emailid']
		invoice = request.form['invoice']
		product = request.form['product']
		remarks = request.form['remarks']
		address = request.form['address']
		states = request.form['states']	
		file = request.files['image']
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
		
		drawing = open('/home/arpan/Desktop/'+file.filename, 'rb')
		
		aluu=drawing.read()

		
		encoded=psycopg2.Binary(aluu)

		try:
			myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
			myConnection.autocommit = True
			cur = myConnection.cursor()
			
		except psycopg2.DatabaseError as e:
			if con:
				con.rollback()

				print(f'Error {e}')


		
		
		region=""
		state=str(states)
		
		






		gmail_user = 'arpanghoshal77@gmail.com'  
		gmail_password = '********'
		
		northemail = 'arpanghoshal@outlook.com'
		southemail = 'arpanghoshal.z@gmail.com'
		eastemail = ''
		westemail = ''

		if region in "north":
			to = [emailid,gmail_user,northemail]
		elif region in "south":
			to = [emailid,gmail_user,southemail]
		elif region in"east":
			to = [emailid,gmail_user,eastemail]
		else:
			to = [emailid,gmail_user,westemail]



		
		sent_from = gmail_user  
		subject = 'OMG Super Important Message'  
		body = 'Hey, whats up?\n\n- You'

		email_text = """\  
		From: %s  
		To: %s  
		Subject: %s

		%s
		%s
		%s
		%s
		%s
		""" % (sent_from, ", ".join(to), subject, body,emailid,invoice,product,remarks)

#.join(to)

		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, email_text)
		server.close()

		
		
		cur.execute("SELECT serialno FROM persons ORDER BY serialno DESC LIMIT 1")
		for serialno1 in cur.fetchall() :
			stud= " ".join(str(serialno1))
		
		stud= stud.replace(' ','')		
		stud= stud.replace(',','')
		stud = stud.replace('(','')
		stud= stud.replace(')','')
		stud = int(stud)
		stud =stud +1
		studcha = stud

		n=stud
		count=0
		while(n>0):
			count=count+1
			n=n//10

		stud = str(stud)

		if count==1:
			stud="0000"+stud
		elif count == 2:
			stud= "000"+stud
		else:
			stud="00"+stud		


		syd1="CMT"+stud	
		syd1= syd1.replace(" ","")
		serialnogenerated = syd1
		status="OPEN"


		
		
		print(encoded,)
		cur.execute( "INSERT INTO persons VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",(emailid,invoice,product,remarks,serialnogenerated,address,state,status,encoded,))


		myConnection.close()




		return ('Complaint sent!')

	else:
		return ('kya chl rha hai bhai')


@app.route("/assigned")
def uploadsoo():
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		myConnection.autocommit = True
		cur = myConnection.cursor()
		susu=""
		cur.execute("SELECT serialnogenerated,state,status FROM persons WHERE status ='ASSIGNED' ORDER BY serialno ASC;")
	
		arrows = cur.fetchall()



		

		myConnection.close()

		
			
		return render_template('hiiitu.html',arrows=arrows)



#4 inspection     1 decision 

@app.route("/closed")
def uploadsooc():
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		myConnection.autocommit = True
		cur = myConnection.cursor()
		susu=""
		cur.execute("SELECT serialnogenerated,state,status FROM persons WHERE status = 'C' ORDER BY serialno ASC;")
	
		arrows = cur.fetchall()



		

		myConnection.close()

		
			
		return render_template('hiiiclo.html',arrows=arrows)


@app.route("/open")
def uploadsooo():
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		myConnection.autocommit = True
		cur = myConnection.cursor()
		susu=""
		cur.execute("SELECT serialnogenerated,state,status FROM persons WHERE status = 'OPEN' ORDER BY serialno ASC;")
	
		arrows = cur.fetchall()



		

		myConnection.close()

		
			
		return render_template('hiiope.html',arrows=arrows)



		
@app.route("/complaints")
def uploadsu():
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		myConnection.autocommit = True
		cur = myConnection.cursor()
		susu=""
		cur.execute("SELECT serialnogenerated, product, emailid,state,status FROM persons ORDER BY serialnogenerated ASC;")
	
		rows = cur.fetchall()
		for a,b,c,d,e in rows :
			aq=a
			bq=b
			cq=c
			dq=d
			eq=e
			

		myConnection.close()
		
		
		return render_template('hiiisu.html',aq=aq,bq=bq,cq=cq,dq=dq,eq=eq,a=a,rows=rows)
		




@app.route("/server/<string:text>", methods=['GET', 'POST'])
def uploadse(text):

		print(text)	
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		myConnection.autocommit = True
		cur = myConnection.cursor()
		susu=""
		cur.execute("SELECT emailid,invoice,product,remarks,serialnogenerated,address,state,status,serialno FROM persons WHERE serialnogenerated = (%s);",(text,))
		
		rows = cur.fetchall()
		for a,b,c,d,e,f,g,h,sno in rows :
			aq=a
			bq=b
			cq=c
			dq=d
			eq=e
			fq=f
			gq=g
			hq=h
			snoq=sno
		
		#print(eq)


	







		cur.execute("SELECT imagess FROM persons WHERE serialnogenerated = (%s); ",(text,))
		blob = cur.fetchone()
		halu = ""
		halu = text
		print(blob)
		open('static/CMT00031.png', 'wb').write(blob[0])
		if request.method == 'POST':
			assignedto= request.form['assignedto']
			assignedto= assignedto.replace(' ','')		
			assignedto = assignedto.replace(',','')
			assignedto = assignedto.replace('(','')
			assignedto= assignedto.replace(')','')


			#print(assignedto,snoq,text)
			cur.execute( "UPDATE persons SET assignedto =  (%s), status = 'ASSIGNED' WHERE serialnogenerated = (%s);",(assignedto,text,))
			return("Work Assigned")
		myConnection.close()

			

		return render_template('hiiis.html',aq=aq,bq=bq,cq=cq,dq=dq,eq=eq,fq=fq,gq=gq,hq=hq,a=a,rows=rows,halu=halu,text=text)
		



@app.route("/serverass/<string:text>", methods=['GET', 'POST'])
def uploadses(text):

		print(text)	
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		myConnection.autocommit = True
		cur = myConnection.cursor()
		susu=""
		cur.execute("SELECT emailid,invoice,product,remarks,serialnogenerated,address,state,status,serialno FROM persons WHERE serialnogenerated = (%s);",(text,))
		
		rows = cur.fetchall()
		for a,b,c,d,e,f,g,h,sno in rows :
			aq=a
			bq=b
			cq=c
			dq=d
			eq=e
			fq=f
			gq=g
			hq=h
			snoq=sno
		
		#print(eq)



		cur.execute("SELECT imagess FROM persons WHERE serialnogenerated = (%s); ",(text,))
		blob = cur.fetchone()
		halu = ""
		halu = eq
		kalu= eq+'.jpg'
		

		if request.method == 'POST':
			productcode= request.form['productcode']
			
			appquan= request.form['appquan']
			remarks= request.form['remarks']
			defectw= request.form['defectw']
			defectw= defectw.replace(' ','')		
			defectw = defectw.replace(',','')
			defectw = defectw.replace('(','')
			defectw = defectw.replace(')','')


			cur.execute( "UPDATE persons SET procodeass =  (%s) ,defectsass = (%s)  , appquanass =  (%s) , remarksass = (%s) , status = 'RESOLVED' WHERE serialnogenerated = (%s);",(productcode,defectw,appquan,remarks,text,))
			return("Complaint Resolved")
		myConnection.close()

			

		return render_template('hiiisas.html',aq=aq,bq=bq,cq=cq,dq=dq,eq=eq,fq=fq,gq=gq,hq=hq,a=a,rows=rows,halu=halu,text=text)




if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
	
