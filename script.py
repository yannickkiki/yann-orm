from core import Condition
from models import Employee

# SQL: SELECT id, first_name, last_name FROM employees;
# employees = Employee.objects.select('id', 'first_name', 'last_name')

# SQL: SELECT salary FROM employees WHERE id <= 3;
# employees = Employee.objects.select('salary', condition=Condition(id__lte=3))

# SQL: SELECT salary FROM employees WHERE id >= 2 AND id<=4;
# employees = Employee.objects.select('salary', condition=Condition(id__gte=2, id__lte=4))
# employees = Employee.objects.select('salary', condition=Condition(id__gte=2) & Condition(id__lte=4))

# SQL: SELECT salary FROM employees WHERE id < 2 OR id>3;
employees = Employee.objects.select('salary', condition=Condition(id__lt=2) | Condition(id__gt=3))

print(employees)
