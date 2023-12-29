from werkzeug.security import generate_password_hash
from models_practica_3_task_6 import db, Users


def add_user_in_database(email: str, username: str, password: str) -> None:

    new_user = Users(email=email,
                     username=username,
                     password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    print('add new user')
