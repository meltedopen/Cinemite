from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash


import models
import forms

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'adkjfalj.adflja.dfnasdf.asd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
    # if current_user.is_authenticated:
    return render_template('layout.html')
    # else:
    #     return render_template('landing.html')


@app.route('/movies')
def movies():
    return render_template('movies.html')


@app.route('/movie/<movieid>', methods=['POST'])
def add_movie(movieid=None):
    print(movieid)
    models.List.create_list_item(current_user.id, movieid)
    return 'success'


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Yay you registered', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                # creates session
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))


@app.route('/list')
@app.route('/list/<username>')
@login_required
def list(username=None):
    from models import List
    if username:
        list = current_user.get_list().limit(100)
        user = current_user
        return render_template('list.html', list=list, user=user)
    return render_template('layout.html')


@app.route('/delete/<movieid>', methods=['POST'])
@login_required
def delete(movieid=None):
    return 'you clicked delete'
    # from models import List
    # if movieid and request.method == 'POST':
    #     return List.delete_list_item()
    # return render_template('list.html')


if __name__ == '__main__':
    models.initialize()

    app.run(debug=DEBUG, port=PORT)
