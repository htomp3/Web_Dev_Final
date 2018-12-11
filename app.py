from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, login_required,UserMixin, LoginManager

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'thisisasecretkeyaaaaaaaaaaaaaaa'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    uname = db.Column(db.String(80))
    password = db.Column(db.String(80))


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
        #print(newClient)
        db.session.add(newClient)
        db.session.commit()
        login_user(newClient)
        return redirect('/index')
    return render_template('create.html')


@app.route('/read', methods=["GET"])
def read():
    clients = Client.query.all()
    return render_template('read.html', clients=clients)

@login_manager.user_loader
def load_user(uid):
    return Client.query.get(uid)

if __name__ == '__main__':
    app.run()
