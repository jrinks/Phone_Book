from app import app, db, mail
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
from app.forms import UserInfoForm, LoginForm, PostForm
from app.models import User, Post

@app.route('/')
def index():
    context = {
       'title': 'HOME',
       'posts': Post.query.all()
    }
    return render_template('index.html', **context)


@app.route('/view_phone_book.html', methods=['GET', 'POST'])
def view_phone_book():
    context = {
       'form' : UserInfoForm(),
       'title': 'VIEW PHONE BOOK',
       'users': User.query.all()
    }
    return render_template('view_phone_book.html', **context)


@app.route('/register_phone_number.html', methods=['GET', 'POST'])
def register_phone_number():
    title = 'REGISTER PHONE NUMBER'
    #UserInfoForm is the name of a class in the forms.py file
    form = UserInfoForm()
    #if the request type of a post and the form validates successfully
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phonenumber = form.phonenumber.data
        #print(username, email, password, firstname, lastname, phonenumber)
  
# Check if usre number already exists
        existing_user = User.query.filter((User.username == username) | (User.phonenumber == phonenumber)).all()
        if existing_user:
            flash('That username or phone number already exists. Please try again', 'danger')
            return redirect(url_for('register_phone_number'))
        
        new_user = User(username, email, password, firstname, lastname, phonenumber)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username} for registering and adding your phone number {phonenumber} to the Phone Book!', 'success')

        msg = Message(f'Thank you, {username}', recipients=[email])
        msg.body = f'Dear {username}, thank you so much for registering your phone number in the Phone Book. I hope you enjoy and also I just wanted to let you know that you are killin\' it today!'
        mail.send(msg)

        return redirect(url_for('index'))

    return render_template('register_phone_number.html', title=title, form=form)


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    title = 'LOGIN'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect Username/Password. Please try again.', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('You have succesfully logged in!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out!', 'primary')
    return redirect(url_for('index'))


@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    title = 'CREATE POST'
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post_title = form.title.data
        post_body = form.body.data
        user_id = current_user.id

        new_post = Post(post_title, post_body, user_id)

        db.session.add(new_post)
        db.session.commit()

        flash(f"You have created a post: {post_title}", 'info')

        return redirect(url_for('index'))

    return render_template('createpost.html', title=title, form=form)
