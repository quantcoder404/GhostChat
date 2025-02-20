from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=False)
    PassWord = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.SrNo} - {self.UserName}"


def init_db():
    with app.app_context():
        db.create_all()
        print("Database and tables created.")


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():  
      if request.method=='POST':
        print("POST request login world")
        UserName = request.form['username']
        PassWord = request.form['password']

        user = User(UserName = UserName, PassWord = PassWord)
        if User.query.filter_by(UserName=UserName, PassWord=PassWord).first():
            return redirect(url_for('display'))
        else:
            return "Invalid credentials"
      return render_template('login.html')



@app.route('/adminData', methods = ['GET', 'POST'])
def admin():  
      allUser = User.query.all()
      return render_template('adminData.html',allUser=allUser)

 
@app.route('/registration', methods = ['GET', 'POST'])
def registration():
      if request.method == 'POST':
        print("POST request")  # Debugging statement  
        UserName = request.form["username"]
        PassWord = request.form["password"]
        user = User(UserName = UserName, PassWord = PassWord)
        if User.query.filter_by(UserName = UserName).first():
            return "User already exists"
        else:
            print("User added successfully")  # Debugging statement
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
      else:  
            print("none hai bhao")# Debugging statement       
        
            return render_template('registration.html')


@app.route('/display')
def display():
    return "display world"


if __name__ == '__main__':
    init_db()  # Initialize the database before running the app
    app.run(debug=True, port=8080)



