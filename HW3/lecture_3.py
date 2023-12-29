from flask import Flask, request, render_template
from models_lecture_3 import db, User, Post
from flask_wtf.csrf import CSRFProtect
from forms_lecture_3 import LoginForm


#import secrets
#secrets.token_hex()


app = Flask(__name__)
app.config['SECRET_KEY'] = b'9a52a511241874c17fbd4e76762aaf677024b6d20f89cf48d3aca53d27de6805'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/')
def index():
    return 'This is the main page'


@app.route('/login/', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        print('форма прошла валидацию')
        print(username)
        print(password)

    return render_template('lecture_3_login.html', form=form)


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = { 'users': users }
    return render_template('lecture_3_all_users.html', **context)


@app.route('/users/<username>/')
def users_by_username(username: str):
    users = User.query.filter(User.username == username).all()
    context = {'users': users}
    return render_template('lecture_3_all_users.html', **context)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Ок')


@app.cli.command("add-user")
def add_user():
    user = User(username='user', email='user@mail.com')
    db.session.add(user)
    db.session.commit()
    print('user add db')


@app.cli.command("edit-user")
def edit_user():
    user = User.query.filter_by(username='user').first()
    user.email = 'new_user@mail.com'
    db.session.commit()
    print('edit user db')


@app.cli.command("del-user")
def del_user():
    user = User.query.filter_by(username='user').first()
    db.session.delete(user)
    db.session.commit()
    print('del user db')


@app.cli.command("fill-db")
def fill_tables():

    count = 5

    for user in range(1, count + 1):
        new_user = User(username=f'user{user}', email=f'user{user}@mail.ru')
        db.session.add(new_user)
    db.session.commit()

    for post in range(1, count ** 2):
        author = User.query.filter_by(username=f'user{post % count + 1}').first()
        new_post = Post(title=f'Post title {post}', content=f'Post content {post}', author=author)
        db.session.add(new_post)
    db.session.commit()


if __name__ == '__main__':
    app.run()
