from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "sampleKey123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


load_dotenv()

password = os.getenv("PASSWORD") 
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "audrius13toto@gmail.com"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PASSWORD"] = password 

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route("/", methods=["GET", "POST"])
def index():
    print(request.method)
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name, last_name, email, date, occupation)

        form = Form(first_name=first_name, last_name=last_name, date=date_obj, email=email, occupation=occupation)
        # SQL insert
        db.session.add(form)
        db.session.commit()
        flash(f"{first_name}, your form was submitted!", "success")

        message_body = f"Thank you, for the submission, {first_name}"
        message = Message(subject="New form submitted.", sender=app.config["MAIL_USERNAME"], recipients=[email], body=message_body)

        mail.send(message) # ADD THIS LINE

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)