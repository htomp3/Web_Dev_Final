from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, login_required,UserMixin, LoginManager

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'thisisasecretkeyaaaaaaaaaaaaaaa'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)

# class Info(db.Model,UserMixin):
#     id=db.Column(db.Integer,primary_key=True)
#     bodyweight=db.Column(db.Integer)
#     bench=db.Column(db.Integer)
#     squat=db.Column(db.Integer)
#     incline=db.Column(db.Integer)
#     deadlift=db.Column(db.Integer)
#     owner_id=db.Column(db.Integer,db.ForeignKey('client.id'))

class Client(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    uname = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    #info=db.relationship('Info',backref='owner')


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
                flash('Username is already taken. Choose another one', 'error')
                return redirect('/create')
            else:
                #print(newClient)
                db.session.add(newClient)
                db.session.commit()

        else:
            flash('Fields cannot be empty. Enter valid data.', 'error')
            return redirect('/create')
        return redirect('/login')
    return render_template('create.html')


@app.route('/read', methods=["GET"])
def read():
    clients = Client.query.all()
    return render_template('read.html', clients=clients)

# @app.route('/Info', methods=["GET", "POST"])
# #@login_required
# def Info():
#     if request.form:
#         print(request.form)
#         bodyweight = int(request.form['bodyweight'])
#         bench = int(request.form['bench'])
#         squat = int(request.form['squat'])
#         incline = int(request.form['incline'])
#         deadlift=int(request.form['deadlift'])
#         newInfo=Info(bodyweight=bodyweight, bench=bench, squat=squat, incline=incline, deadlift=deadlift)
#         db.session.add(newInfo)
#         db.session.commit()
#         return redirect('/read')
#     return render_template('Info.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        password=request.form['password']
        client=Client.query.filter_by(uname=uname,password=password).first()
        if client is None:
            flash('Username or Password is invalid', 'error')
            return redirect('/login')
        login_user(client)
        return render_template('read.html')
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
