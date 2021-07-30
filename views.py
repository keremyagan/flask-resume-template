from flask import Flask,render_template,redirect,url_for,request,make_response,session
from itsdangerous import Signer ,BadSignature
from session_interface import MySessionInterface
from flask_mail import Mail,Message
import yaml

y = yaml.safe_load(open("config.yml").read())
app=Flask(__name__)
sender_mail=y["sender_mail"]
mail_password=y["mail_password"]
receiver_mail=y["receiver_mail_address"]
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = sender_mail,
	MAIL_PASSWORD = mail_password
	)
mail = Mail(app)
app.secret_key= y["app_secret_key"] 
app.session_interface = MySessionInterface()

@app.route("/homepage")
def Index():
    return render_template("index.html")

@app.route("/mail-success",methods=["POST"])
def mails():
    name=request.form["name"]
    email=request.form["_replyto"]
    message=request.form["message"]
    ContextData={
    "name":name,
    "email":email,
    "message":message,  
    }
    msg = Message("Yeni Bildiri Var!",
                  sender=sender_mail,
                  recipients=receiver_mail)
    msg.body=f"İsim:{name}\nEmail:{email}\nMesaj:{message} "
    mail.send(msg)
    return render_template("mail-success.html",**ContextData)

app.run(debug=True)