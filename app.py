from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_ckeditor import CKEditor, CKEditorField
from peewee import fn


import models
import forms

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'adkjfalj.adflja.dfnasdf.asd'
ckeditor = CKEditor(app)
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
    return render_template('landing.html')
    # else:
    #     return render_template('landing.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/movies')
def movies():
    return render_template('movies.html')


@app.route('/movie/<movieid>/update', methods=['POST', 'GET'])
def update_comment(movieid):
    movie_id = int(movieid)
    form = forms.CommentForm()
    list_item = models.List.select().where(models.List.user == current_user.id,
                                           models.List.movie_id == movie_id).get()
    list_item.comment = form.comment.data
    list_item.save()
    return redirect(url_for('movie', movieid=movieid))


def comments_list(movieid):
    movie_id = int(movieid)
    from models import List
    query = List.select(List.comment).where(List.movie_id == movie_id)
    for list in query:
        print(list.comment)
    return redirect(url_for('movie', movieid=movieid, query=query))


@app.route('/movie/<movieid>', methods=['POST'])
def add_movie(movieid=None):
    models.List.create_list_item(current_user.id, movieid)
    flash('This movie has been added to your watch list.', 'success')
    return 'success'


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('You have successfully registered for Cinemite!', 'success')
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
            flash("This user does not exist.", "danger")
        else:
            if check_password_hash(user.password, form.password.data):
                # creates session
                login_user(user)
                flash("You have successfully logged into Cinemite!", "success")
                return redirect(url_for('movies'))
            else:
                flash("Your email or password is incorrect.", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out of Cinemite.", "success")
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username=None):
    user = models.User.select().where(models.User.username == username).get()
    return render_template('user.html', user=user)


@app.route('/user/<userid>/update', methods=['GET', 'POST'])
@login_required
def update_user(userid=None):
    form = forms.UserForm()
    user_id = int(userid)
    user = models.User.get(current_user.id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.save()
        return redirect(url_for('user', username=user.username))
    return render_template('edit-user.html', form=form, userid=userid)


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


@app.route('/delete/<movieid>/user/<userid>', methods=['POST'])
@login_required
def delete(movieid=None, userid=None):
    list = models.List.select().where(models.List.user == userid,
                                      models.List.movie_id == movieid).get()
    list.delete_instance()
    return redirect(url_for('list', username=current_user.username))


@app.route('/update/<movieid>/user/<userid>', methods=['POST'])
@login_required
def update(movieid=None, userid=None):
    list = models.List.select().where(models.List.user == userid,
                                      models.List.movie_id == movieid).get()
    if list.watched == 0:
        list.watched = 1
        list.save()
        return redirect(url_for('list', username=current_user.username))
    if list.watched == 1:
        list.watched = 0
        list.save()
        return redirect(url_for('list', username=current_user.username))
    return redirect(url_for('list', username=current_user.username))


@app.route('/movie/<movieid>', methods=['GET', 'POST'])
@login_required
def movie(movieid=None):
    from models import List
    form = forms.CommentForm()
    if movieid and request.method == 'GET':
        movie_id = int(movieid)
        from models import List, User
        query = (List.select(List.comment, User.username).join(User).where(
            User.id == List.user)).where(List.movie_id == movie_id and fn.length(List.comment) > 0)
        return render_template('movie.html', form=form, movieid=movieid, query=query)
    elif movieid and request.method == 'POST':
        comment = models.List.select().where(models.List.user == current_user,
                                             models.List.movie_id == movieid).get()
        comment.comment = form.comment.datas


if __name__ == '__main__':
    models.initialize()

    app.run(debug=DEBUG, port=PORT)
