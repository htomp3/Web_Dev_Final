from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, login_required, UserMixin, LoginManager, current_user

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'thisisasecretkeyaaaaaaaaaaaaaaa'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)

class Client(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    uname = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    bodyweight = db.Column(db.Integer, nullable=False)
    bench = db.Column(db.Integer, nullable=False)
    squat = db.Column(db.Integer, nullable=False)
    incline = db.Column(db.Integer, nullable=False)
    deadlift = db.Column(db.Integer, nullable=False)



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
        bodyweight = int(request.form['bodyweight'])
        bench = int(request.form['bench'])
        squat = int(request.form['squat'])
        incline = int(request.form['incline'])
        deadlift = int(request.form['deadlift'])
        if fname!='' and lname!="" and uname!="" and password!="" and bodyweight!="" and bench!="" and \
            squat!="" and incline!="" and deadlift !="" :
            newClient = Client(fname=fname, lname=lname, uname=uname, password=password,
                               bodyweight=bodyweight, bench=bench, squat=squat, incline=incline, deadlift=deadlift)
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
        flash('You have successfully created an account and can login!')
        return redirect('/login')
    return render_template('create.html')


@app.route('/read', methods=["GET"])
def read():
    clients=Client.query.all()
    return render_template('read.html', clients=clients)


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
        return redirect('/profile')
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

        bodyweight=temp.bodyweight
        bench=temp.bench
        squat=temp.squat
        incline=temp.incline
        deadlift=temp.deadlift
        return render_template('update.html',id=id, fname=fname, lname=lname, uname=uname, password=password,
                               bodyweight=bodyweight, bench=bench, squat=squat, incline=incline, deadlift=deadlift)

    if request.method == "POST":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        temp.fname = request.form['newfname']
        temp.lname = request.form['newlname']
        temp.uname = request.form['newuname']
        temp.password = request.form['newpassword']

        temp.bodyweight=int(request.form['newbodyweight'])
        temp.bench = int(request.form['newbench'])
        temp.squat = int(request.form['newsquat'])
        temp.incline = int(request.form['newincline'])
        temp.deadlift = int(request.form['newdeadlift'])
        db.session.commit()
        return redirect('/profile')


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

        bodyweight = temp.bodyweight
        bench = temp.bench
        squat = temp.squat
        incline = temp.incline
        deadlift = temp.deadlift
        return render_template('delete.html', id=id, fname=fname, lname=lname, uname=uname, password=password,
                               bodyweight=bodyweight, bench=bench, squat=squat, incline=incline, deadlift=deadlift)

    if request.method == "POST":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        if request.form['option'] == 'yes':
            db.session.delete(temp)
            db.session.commit()
        return redirect('/read')

@app.route('/profile')
@login_required
def profile():
    uname=current_user
    client = Client.query.filter_by(uname=uname.uname).first()
    return render_template('profile.html', client=client)

@login_manager.user_loader
def load_user(uid):
    return Client.query.get(uid)

if __name__ == '__main__':
    app.run()
