from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint


db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100),  nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(200), nullable=False)
    information_about_ratings = db.relationship('Evaluation', backref='students')

    def __repr__(self):
        return f'Student({self.name}, {self.surname}, {self.group}, {self.email})'


class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    estimation = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('estimation > 0', name='check_estimation_min'),
        CheckConstraint('estimation <= 5', name='check_estimation_max'),
    )

    def __repr__(self):
        return f'Evaluation({self.item_name}, {self.estimation})'
