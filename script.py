from core import Condition
from models import Employee

# employees = Employee.objects.select('id', 'first_name', 'last_name')
employees = Employee.objects.select('salary', condition=Condition())
print(employees)
