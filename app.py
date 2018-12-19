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

class Client(db.Model,UserMixin):#owner
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    uname = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    workouts = db.relationship('Workout', backref='client')


class Workout(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bodyweight = db.Column(db.Integer, nullable=False)
    bench = db.Column(db.Integer, nullable=False)
    squat = db.Column(db.Integer, nullable=False)
    incline = db.Column(db.Integer, nullable=False)
    deadlift = db.Column(db.Integer, nullable=False)

    workout_id = db.Column(db.Integer, db.ForeignKey('client.id'))




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
        newClient = Client(fname=fname, lname=lname, uname=uname, password=password)
        user=Client.query.filter_by(uname=uname).first()
        if user is not None:
            flash('Username is already taken. Choose another one', 'error')
            return redirect('/create')
        else:
            #print(newClient)
            db.session.add(newClient)
            db.session.commit()
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
            flash('Username or Password is invalid')
            return redirect('/login')
        login_user(client)
        flash('Successfully logged in')
        return redirect('/profile')
    return render_template('login.html')


@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    user=current_user
    if request.form:
        print(request.form)
        bodyweight = int(request.form['bodyweight'])
        bench = int(request.form['bench'])
        squat = int(request.form['squat'])
        incline = int(request.form['incline'])
        deadlift = int(request.form['deadlift'])

        if bodyweight>0 and bench>0 and squat >0 and incline >0 and deadlift >0:
            clientInfo = Workout(bodyweight=bodyweight, bench=bench, squat=squat, incline=incline, deadlift=deadlift)
            clientInfo.client=user
            db.session.add(clientInfo)
            db.session.commit()
            flash('Your One Rep Maxes have been logged!')
        else:
            flash('You must enter data greater than 0')
            return redirect('/info')
        return redirect('/readinfo')
    return render_template('info.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out. Come back soon.')
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

        flash('Account successfully updated')
        return render_template('update.html',id=id, fname=fname, lname=lname, uname=uname, password=password)

    if request.method == "POST":
        print(var)
        temp = Client.query.filter_by(id=var).first()

        temp.fname = request.form['newfname']
        temp.lname = request.form['newlname']
        temp.uname = request.form['newuname']
        temp.password = request.form['newpassword']

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

        return render_template('delete.html', id=id, fname=fname, lname=lname, uname=uname, password=password)

    if request.method == "POST":
        print(var)
        temp = Client.query.filter_by(id=var).first()
        if request.form['option'] == 'yes':
            db.session.delete(temp)
            db.session.commit()
            flash('Account successfully deleted')
            return redirect('/login')
        flash('Hell yeah brother, keep getting those gains')
        return redirect('/profile')

@app.route('/profile')
@login_required
def profile():
    uname=current_user
    client = Client.query.filter_by(uname=uname.uname).first()
    return render_template('profile.html', client=client)

@app.route('/readinfo')
@login_required
def readinfo():
    uname=current_user
    workout = Workout.query.filter_by(id=uname.id).first()
    return render_template('readinfo.html', workout=workout)

@app.route('/updateinfo/<var>', methods=["GET", "POST"])
def updateinfo(var):
    if request.method == "GET":
        print(var)
        temp = Workout.query.filter_by(id=var).first()
        id = temp.id
        bodyweight = temp.bodyweight
        bench = temp.bench
        squat = temp.squat
        incline = temp.incline
        deadlift=temp.deadlift
        flash('Hell yeah, log that progress brother!')
        return render_template('updateinfo.html',id=id, bodyweight=bodyweight, bench=bench, squat=squat, incline=incline, deadlift=deadlift)

    if request.method == "POST":
        print(var)
        temp = Workout.query.filter_by(id=var).first()
        temp.bodyweight = int(request.form['newbodyweight'])
        temp.bench = int(request.form['newbench'])
        temp.squat = int(request.form['newsquat'])
        temp.incline = int(request.form['newincline'])
        temp.deadlift=int(request.form['newdeadlift'])

        db.session.commit()
        return redirect('/readinfo')

@login_manager.user_loader
def load_user(uid):
    return Client.query.get(uid)

@app.errorhandler(404)
def err404(err):
    return render_template('error.html',err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('error.html',err=err)


if __name__ == '__main__':
    app.run()
