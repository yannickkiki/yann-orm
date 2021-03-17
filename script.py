from models import Employee

employees = Employee.get_objects_manager().select('first_name', 'last_name', 'salary')
print(employees)
