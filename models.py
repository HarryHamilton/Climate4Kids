# created 4/12/2021 by Josh Oppenheimer
# model of the database. Has constructors for handling the database information within python
# (Will change as we change that details of variables and table interaction)

from app import db


# parent class of Student and Teacher, user_type defines which of the two they are.
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), autoincrement=True, nullable=False, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    last_login = db.Column(db.String(50))
    registered_on = db.Column(db.String(50), nullable=False)

    __mapper_args_ = {'polymorphic_identity': 'users', 'polymorphic_on': user_type}

    # constructor
    def __init__(self, user_type, name, username, password, last_login, registered_on):
        self.user_type = user_type
        self.name = name
        self.username = username
        self.password = password
        self.lastLogin = last_login
        self.registered_on = registered_on

    # string representation
    def __repr__(self):
        return '<User %r>' % self.username


# NOTE: group_id is used by both student and teacher and could be made a user property instead
class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    quiz_id = db.Column(db.Integer(), autoincrement=True, nullable=False, primary_key=True)
    group_id = db.Column(db.ForeignKey('groups.id'))

    # relationships
    quizzes = db.relationship('Quiz')

    __mapper_args__ = {'polymorphic_identity': 'student'}

    def __init__(self, user_type, name, username, password, last_login, registered_on, group_id):
        super().__init__(user_type, name, username, password, last_login, registered_on)
        self.group_id = group_id


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    group_id = db.Column(db.ForeignKey('groups.id'))

    __mapper_args__ = {'polymorphic_identity': 'teacher'}

    def __init__(self, user_type, name, username, password, last_login, registered_on,
                 group_id):
        super().__init__(user_type, name, username, password, last_login, registered_on)
        self.group_id = group_id


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer(), autoincrement=True, nullable=False, primary_key=True)
    group_code = db.Column(db.String(10), nullable=False)
    key_stage = db.Column(db.String(10), nullable=False)

    def __init__(self, group_code, key_stage):
        self.group_code = group_code
        self.key_stage = key_stage

    # relationships
    students = db.relationship('Student')
    # used backref to allow the relationship to be many (group) to one (teacher)
    teachers = db.relationship('Teacher', backref='groups')


class Quiz(db.Model):
    __tabelname__ = 'quizzes'
    id = db.Column(db.Integer(), autoincrement=True, nullable=False, primary_key=True)
    score = db.Column(db.Integer(), nullable=False)
    student_id = db.Column(db.ForeignKey('student.id'))

    def __init__(self, score, student_id):
        self.score = score
        self.student_id = student_id


def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    # test = User("student", "James", "james02", "testing", "111", "1111")
    # db.session.add(test)
    db.session.commit()
