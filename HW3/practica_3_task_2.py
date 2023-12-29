"""
Задание №2
- Создать базу данных для хранения информации о книгах в библиотеке.
- База данных должна содержать две таблицы: "Книги" и "Авторы".
- В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
- В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
- Необходимо создать связь между таблицами "Книги" и "Авторы".
- Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.
"""
from models_practica_3_task_2 import db, Books, Authors
from flask import Flask, render_template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


#with app.app_context():
#    db.create_all()


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('database has been created')


@app.cli.command("add-book")
def add_students():

    count: int = 5

    for book in range(1, count + 1):
       new_book = Books(title=f'title_book_{book}',
                        year_publication=book,
                        number_instances=book,
                        author_id=book)
       db.session.add(new_book)
    db.session.commit()

    for author in range(1, count + 1):
        new_author = Authors(name=f'author_name_{author}',
                             surname=f'author_surname_{author}')
        db.session.add(new_author)
    db.session.commit()
    print('database is full')


@app.route('/')
def index():

    books = Books.query.all()
    author_two = Authors.query.get(2)

    context = {
        'title_pag': 'Вывод информации о книгах',
        'books': books,
        'author_two': author_two
    }
    return render_template('practica_3_task_2_all_books.html', **context)


if __name__ == '__main__':
    app.run()
