from flask import Flask, jsonify, request
from models import db, Employee
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Union

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db.init_app(app)

# create the database tables
# db.create_all()
with app.app_context():
    db.create_all()

@app.route('/emp', methods=['GET'])
def get_all_employees() -> List[Dict[str, Union[int, str, float]]]:
    """
    Retrieve all employees.
    Returns:
        list: A list of dictionaries representing each employee.
    """
    employees = Employee.query.all()
    print("EMPM", employees)
    return jsonify([{'EmpNo': emp.EmpNo, 'EmpName': emp.EmpName, 'sal': emp.sal} for emp in employees])

@app.route('/emp/<int:id>', methods=['GET'])
def get_employee_by_id(id: int) -> Dict[str, Union[int, str, float]]:
    """
    Retrieve a specific employee by EmpNo.
    Args:
        id (int): The EmpNo of the employee to retrieve.
    Returns:
        dict: A dictionary representing the employee.
    """
    employee = Employee.query.filter_by(EmpNo=id).first()
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify({'EmpNo': employee.EmpNo, 'EmpName': employee.EmpName, 'sal': employee.sal})

@app.route('/emp', methods=['POST'])
def create_employee() -> Dict[str, str]:
    """
    Create a new employee.
    Returns:
        dict: A message indicating the success of the operation.
    """
    data = request.json
    employee = Employee(EmpNo=data['EmpNo'], EmpName=data['EmpName'], sal=data['sal'])
    try:
        db.session.add(employee)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Employee with the same EmpNo already exists'}), 400
    return jsonify({'message': 'Employee created successfully'})

@app.route('/emp/<int:id>', methods=['PUT'])
def update_employee(id: int) -> Dict[str, str]:
    """
    Update an existing employee by EmpNo.
    Args:
        id (int): The EmpNo of the employee to update.
    Returns:
        dict: A message indicating the success of the operation.
    """
    data = request.json
    employee = Employee.query.filter_by(EmpNo=id).first()
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404
    employee.EmpName = data.get('EmpName', employee.EmpName)
    employee.sal = data.get('sal', employee.sal)
    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/emp/<int:id>', methods=['DELETE'])
def delete_employee(id: int) -> Dict[str, str]:
    """
    Delete an employee by EmpNo.
    Args:
        id (int): The EmpNo of the employee to delete.
    Returns:
        dict: A message indicating the success of the operation.
    """
    employee = Employee.query.filter_by(EmpNo=id).first()
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
