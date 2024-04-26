import pytest
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import app
from models import db, Employee

@pytest.fixture
def populate_db():
    with app.app_context():
        db.create_all()
        employee = Employee(EmpNo=1, EmpName='Shainkey', sal=20000)
        db.session.add(employee)
        db.session.commit()
    yield
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_all_employees(client):
    response = client.get('/emp')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_get_employee_by_id(client):
    response = client.get('/emp/1')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.json
    assert data['EmpNo'] == 1
    assert data['EmpName'] == 'John Doe'
    assert data['sal'] == 50000

# Add more test cases for other routes...

