from models_practica_3_task_7 import db, Users


def add_user_in_database(name: str, surname: str, email: str, password: str) -> None:

    new_user = Users(name=name, surname=surname, email=email)
    new_user.set_password(password=password)
    db.session.add(new_user)
    db.session.commit()
    print('add new user')
