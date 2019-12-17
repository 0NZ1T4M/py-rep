from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth

from post import Post
from comment import Comment
from category import Category
from user import User

app = Flask(__name__)


auth = HTTPBasicAuth()

@app.route('/')
def hello_world():
    return redirect("/categories")
@@ -43,6 +48,7 @@ def edit_post(id):


@app.route('/posts/new', methods=['GET', 'POST'])
@auth.login_required
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', categories=Category.all())
@@ -102,3 +108,31 @@ def get_category(id):
def delete_category(id):
    Category.find(id).delete()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password'])
        )
        User(*values).create()

        return redirect('/')


@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)
    if user:
        return user.verify_password(password)

    return False


if __name__ == '__main__':
    app.run()
