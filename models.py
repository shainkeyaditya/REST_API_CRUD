from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EmpNo = db.Column(db.Integer, unique=True, nullable=False)
    EmpName = db.Column(db.String(100), nullable=False)
    sal = db.Column(db.Float, nullable=False)
