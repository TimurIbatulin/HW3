"""
Задание №5
- Создать форму регистрации для пользователя.
- Форма должна содержать поля: имя, электронная почта,
пароль (с подтверждением), дата рождения, согласие на
обработку персональных данных.
- Валидация должна проверять, что все поля заполнены
корректно (например, дата рождения должна быть в
формате дд.мм.гггг).
- При успешной регистрации пользователь должен быть
перенаправлен на страницу подтверждения регистрации.
"""
from flask import Flask, flash, request, render_template, redirect, url_for
from practica_3_task_5_add_user_in_database import add_user_in_database
from forms_practica_3_task_5 import UserRegistration
from sqlalchemy.exc import IntegrityError
from models_practica_3_task_5 import db
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

    if request.method == 'POST' \
            and form.validate() \
            and form.consent_processing_personal_data.data:

        username = form.username.data
        date = form.date.data
        email = form.email.data
        password = form.password.data
        #confirm_password = form.confirm_password.data
        #consent_processing_personal_data = form.consent_processing_personal_data.data

        #print('форма прошла валидацию')
        #print(username)
        #print(date)
        #print(email)
        #print(password)
        #print(confirm_password)
        #print(consent_processing_personal_data)

        try:
            add_user_in_database(email=email,
                                 username=username,
                                 password=password,
                                 user_date_birth=date)

            flash(f'Пользователь {username} успешно зарегистрирован !')

            return redirect(url_for('successful_registration_user'))

        except IntegrityError as error:

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

    return render_template('practica_3_task_5_user_registration.html',
                           **context,
                           form=form)


@app.route('/successful_registration_user/')
def successful_registration_user():
    context = {
        'title_pag': 'Поздравление с успешной регистрацией'
    }
    return render_template('practica_3_task_5_successful_registration_user.html', **context)


if __name__ == '__main__':
    app.run()
