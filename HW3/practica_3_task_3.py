"""
Задание №3
- Доработаем задачу про студентов
- Создать базу данных для хранения информации о студентах и их оценках в
учебном заведении.
- База данных должна содержать две таблицы: "Студенты" и "Оценки".
- В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа
и email.
- В таблице "Оценки" должны быть следующие поля: id, id студента, название
предмета и оценка.
- Необходимо создать связь между таблицами "Студенты" и "Оценки".
- Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их оценок.
"""
from models_practica_3_task_3 import db, Students, Evaluation
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


@app.cli.command("add-students-and-evaluation")
def add_students():

    count: int = 5

    for student in range(1, count + 1):
       new_students = Students(name=f'student_name_{student}',
                               surname=f'student_surname_{student}',
                               group=student,
                               email=f'student_email_{student}')
       db.session.add(new_students)
    db.session.commit()

    for student in range(1, count + 1):
        for estimation in range(1, count + 1):
            estimation_student = Evaluation(id_student=student,
                                     item_name='Physics',
                                     estimation=estimation)
            db.session.add(estimation_student)
    db.session.commit()
    print('database is full')


@app.route('/')
def index():

    students = Students.query.all()

    context = {
        'title_pag': 'Вывод информации о студентах',
        'students': students
    }
    return render_template('practica_3_task_3_all_students.html', **context)


if __name__ == '__main__':
    app.run()
