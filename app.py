from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, login_required,UserMixin, LoginManager
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.routing import ValidationError

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'thisisasecretkeyaaaaaaaaaaaaaaa'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    uname = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


# class Info(db.Model,UserMixin):
#     id=db.Column(db.Integer,primary_key=True)
#     bodyweight=db.Column(db.Integer)
#     # bench=
#     # squat=
#     # incline=
#     # deadlift=


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
@app.route('/create', methods=["GET", "POST"])
def create():
    if request.form:
        print(request.form)
        fname = request.form['fname']
        lname = request.form['lname']
        uname = request.form['uname']
        password = request.form['password']
        if fname!='' and lname!="" and uname!="" and password!="":
            newClient = Client(fname=fname, lname=lname, uname=uname, password=password)
            user=Client.query.filter_by(uname=uname).first()
            if user is not None:
                return render_template("unameError.html")
            else:
                #print(newClient)
                db.session.add(newClient)
                db.session.commit()
        else:
            return render_template("logerr.html")
        #login_user(newClient)
        return redirect('/login')
    return render_template('create.html')


@app.route('/read', methods=["GET"])
def read():
    clients = Client.query.all()
    return render_template('read.html', clients=clients)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        password=request.form['password']
        client=Client.query.filter_by(uname=uname).first()
        if client !=None:
            if password==client.password:
                login_user(client)
                return redirect('/index')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/update/<var>', methods=["GET", "POST"])
def update(var):
    if request.method == "GET":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        id = temp.id
        fname = temp.fname
        lname = temp.lname
        uname = temp.uname
        password = temp.password
        return render_template('update.html',id=id, fname=fname, lname=lname,uname=uname, password=password)

    if request.method == "POST":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        temp.fname = request.form['newfname']
        temp.lname = request.form['newlname']
        temp.uname = request.form['newuname']
        temp.password = request.form['newpassword']
        db.session.commit()
        return redirect('/read')


@app.route('/delete/<var>', methods=["GET", "POST"])
def delete(var):
    if request.method == "GET":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        id = temp.id
        fname = temp.fname
        lname = temp.lname
        uname = temp.uname
        password = temp.password
        return render_template('delete.html', id=id,fname=fname, lname=lname,uname=uname, password=password)

    if request.method == "POST":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        if request.form['option'] == 'yes':
            db.session.delete(temp)
            db.session.commit()
        return redirect('/read')


@login_manager.user_loader
def load_user(uid):
    return Client.query.get(uid)

if __name__ == '__main__':
    app.run()
