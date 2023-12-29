"""
Задание №4
Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
- Имя пользователя (обязательное поле)
- Электронная почта (обязательное поле, с валидацией на корректность ввода email)
- Пароль (обязательное поле, с валидацией на минимальную длину пароля)
- Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.
"""
from practica_3_task_4_add_user_in_database import add_user_in_database
from flask import Flask, flash, request, render_template
from forms_practica_3_task_4 import UserRegistration
from sqlalchemy.exc import IntegrityError
from models_practica_3_task_4 import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = b'5114265fa13aa792816230ca645363c24d6fcb2633fd9c18a025a0fe6097a612'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
csrf = CSRFProtect(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('database has been created')


@app.route('/', methods=['GET', 'POST'])
def index():

    form = UserRegistration()

    if request.method == 'POST' and form.validate():

        username = form.username.data
        email = form.email.data
        password = form.password.data
        #confirm_password = form.confirm_password.data

        #print('форма прошла валидацию')
        #print(username)
        #print(email)
        #print(password)
        #print(confirm_password)

        try:
            add_user_in_database(email=email,
                                 username=username,
                                 password=password)
            flash(f'Пользователь {username} успешно зарегистрирован !')
        except IntegrityError as error:
            #flash(f'Пользователь {username} с электронной почтой {email} уже зарегестрирован')

            error_code = error.orig.args[0]

            if 'UNIQUE' in error_code and 'email' in error_code:
                flash(f'Пользователь {username} с такой электронной почтой {email} уже зарегестрирован')

            if 'UNIQUE' in error_code and 'username' in error_code:
                flash(f'Пользователь {username} с таким ником уже зарегестрирован')

        except:
            flash(f'Пользователь {username} НЕ зарегистрирован (произошла ошибка) !')

    context = {
        'title_pag': 'Регистрация пользователя'
    }

    return render_template('practica_3_task_4_user_registration.html',
                           **context,
                           form=form)


if __name__ == '__main__':
    app.run()
