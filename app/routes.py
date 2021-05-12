from app import app
# render_template is a module that says "render this in html"
from flask import render_template, request
from app.forms import UserInfoForm
from app.models import User

#we have a @route for each page of our site
#'/' is our index page
@app.route('/')
def index():
    #context is a global variable that stores values specific to each request. In this case it is a dictionary that holds our list of fruits
    context = {
       'title': 'HOME',
       'items': ['apple', 'banana', 'orange', 'pear', 'watermelon', 'grapefruit', 'grapes'],
       'user': {
            'id': 2,
            'username': 'Brian'
        }  
    }
    #this is where you tell it which template to use and you pass it the info listed above saved in context.  **
    return render_template('index.html', **context)


@app.route('/register_phone_number.html', methods=['GET', 'POST'])
def register_phone_number():
    title = 'REGISTER PHONE NUMBER'
    #UserInfoForm is the name of a class in the forms.py file
    form = UserInfoForm()
    #if the request type of a post and the form validates successfully
    if request.method == 'POST':
        firstname = form.firstname.data
        lastname = form.lastname.data
        phonenumber = form.phonenumber.data
        print(firstname, lastname, phonenumber)
  
# Check if phone number already exists
        existing_phone = User.query.filter(User.phonenumber == phonenumber).all()
        if existing_phone:
            flash('That phone number has already been entered into the phone book.Please try again', 'danger')
            return redirect(url_for('register_phone_number.html'))
        
        new_phone = User(firstname, lastname, phonenumber)
        db.session.add(new_phone)
        db.session.commit()
        flash(f'Thank you {firstname} {lastname} for adding your phone number!', 'success')
        return redirect(url_for('index'))
    
    
    return render_template('register_phone_number.html', title=title, form=form)