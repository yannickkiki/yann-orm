from models import Employee

employees = Employee.objects.select('id', 'first_name', 'last_name')
print(employees)
