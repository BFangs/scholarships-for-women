from jinja2 import StrictUndefined
from flask import (Flask, session, render_template, request, jsonify)
import hashlib
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db
from gevent.wsgi import WSGIServer
from model import (Scholarship, User, Category, ScholarshipCategory, UserCategory, UserScholarship)

app = Flask(__name__)
app.secret_key = "GOFEMINISM"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def display_homepage():
    """displays homepage"""

    scholarships= Scholarship.query.all()
    scholarships_list = []
    for scholarship in scholarships:
        scholarship_id = scholarship.scholarship_id
        scholarship_categories = ScholarshipCategory.query.filter(Scholarship.scholarship_id==scholarship_id).all()
        category_list =[]
        for sc in scholarship_categories:
            category_list.append(sc.categories.category_name)
        scholarships_list.append((scholarship, category_list))

    return render_template('home.html', scholarships=scholarships_list)


@app.route('/login', methods=["POST"])
def login():
    """logs in user"""

    email = request.form.get('email').lower()
    password = request.form.get('password')
    user = User.query.filter(User.email==email).first()
    if user:
        password = password.encode('utf8') 
        hashedpass = q.password.encode('utf8') 
        if bcrypt.checkpw(password, hashedpass):
            session['user_id'] = user.user_id
            return redirect('/')
    else:
        flash("Username or password not found")
        return redirect ('/login')


@app.route('/logout', methods=['POST'])
def logout():
    """logs out user"""

    del session['user_id']

    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    """registers a new user"""

    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    new_user = User(email=email, password=password, name=name)
    db.add(new_user)
    db.commit()

    session['user_id'] = new_user.user_id


@app.route('/save', methods = ['POST'])
def save_scholarship():
    """save scholarship to user's profile"""

    scholarship_id = request.form.get("scholarship_id")

    if 'user_id' in session:
        user_scholarship = UserScholarship(scholarship_id, user_id) 
        db.add(user_scholarship)
        db.commit()

    else:
        flash("Login to save")
        return redirect('/login')


# @app.route('/users')
# @app.route('/scholarships')
"""Boya, you can do either of these two"""


@app.route('/add_category')
def add_user_category():
    """adds a category to user profile"""

    categories = request.form.getlist('categories')

    user_id = session['user_id']

    for category in categories:
        category = Category.query.filter(Category.name==category).first()
        user_category = UserCategory(user_id= user_id, category_id = category.category_id)
        db.add(user_category)
        db.commit()

@app.route('/get_user_scholar')
def get_users_scholarship():
    """"""

    # scholarships =[]

    # user_categories = UserCategory.query.filter_by(user_id==session['user_id']).all()
    # for user_category in user_categories:
    #     category_id=user_category.category_id
    #     scholarship_categories = ScholarshipCategory.query.filter(category_id==category_id).all()
    #     for scholarship in scholarship_categories:




if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    DebugToolbarExtension(app)
