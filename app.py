from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from form import LoginForm, RegisterForm
from model import db, login, UserModel

app = Flask(__name__)
app.secret_key = "a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("home.html")


@app.route("/")
def redirect_to_login():
    return redirect("/login")


def add_user(email, first_name, last_name, username, password):
    user = UserModel.query.filter_by(username=username).first() 
    if user is None:
        user = UserModel()
        user.set_password(password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        db.session.add(user)
        db.session.commit()


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = UserModel.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect('/dashboard')
        else:
            flash('username or password is incorrect')
            return redirect('/login')
    return render_template("/login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        user = UserModel.query.filter_by(email=email).first()
        if user is not None:
            flash("Email already exists.", 'error')
            return redirect('/register')
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            flash("Username already exists.", 'error')
            return redirect('/register')    
        add_user(email=email, first_name=first_name, last_name=last_name, username=username, password=password)
        flash(f"Thank you for registering, {first_name}!", 'success')
        return redirect('/login')
    return render_template("/register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)