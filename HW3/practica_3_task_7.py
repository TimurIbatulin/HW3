"""
Задание №7
- Создайте форму регистрации пользователей в приложении Flask. Форма должна
содержать поля: имя, фамилия, email, пароль и подтверждение пароля. При отправке
формы данные должны валидироваться на следующие условия:
○ Все поля обязательны для заполнения.
○ Поле email должно быть валидным email адресом.
○ Поле пароль должно содержать не менее 8 символов, включая хотя бы одну букву и
одну цифру.
○ Поле подтверждения пароля должно совпадать с полем пароля.
○ Если данные формы не прошли валидацию, на странице должна быть выведена
соответствующая ошибка.
○ Если данные формы прошли валидацию, на странице должно быть выведено
сообщение об успешной регистрации.
"""
from practica_3_task_7_add_user_in_database import add_user_in_database
from flask import Flask, flash, request, render_template
from forms_practica_3_task_7 import UserRegistration
from sqlalchemy.exc import IntegrityError
from models_practica_3_task_7 import db
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

        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        #confirm_password = form.confirm_password.data

        #print('форма прошла валидацию')
        #print(name)
        #print(surname)
        #print(email)
        #print(password)
        #print(confirm_password)

        try:
            add_user_in_database(name=name, surname=surname,
                                 email=email, password=password)

            flash(f'Пользователь {name} {surname} успешно зарегистрирован !')

        except IntegrityError as error:

            error_code = error.orig.args[0]

            if 'UNIQUE' in error_code and 'email' in error_code:
                flash(f'Пользователь {name} {surname} с такой электронной почтой {email} уже зарегестрирован.'
                      f'Электронная почта не должна повторяться у разных пользователей.')

        except:

            flash(f'Пользователь {name} {surname} НЕ зарегистрирован (произошла ошибка) !')

    context = {
        'title_pag': 'Регистрация пользователя'
    }
    return render_template('practica_3_task_5_user_registration.html',
                           **context, form=form)


if __name__ == '__main__':
    app.run()
