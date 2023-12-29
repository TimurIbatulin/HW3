from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year_publication = db.Column(db.Integer,  nullable=False)
    number_instances = db.Column(db.Integer,  nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    information_about_authors = db.relationship('Authors', backref='books')

    def __repr__(self):
        return f'Books({self.id}, {self.title}, {self.year_publication}, {self.number_instances}, ' \
               f'{self.information_about_authors.name}, {self.information_about_authors.surname})'


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100),  nullable=False)

    def __repr__(self):
        return f'Authors({self.name}, {self.surname})'
