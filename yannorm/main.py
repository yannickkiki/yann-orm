from core import Condition
from models import Employee

# SQL: SELECT id, first_name, last_name FROM employees;
# employees = Employee.objects.select('id', 'first_name', 'last_name')

# SQL: SELECT salary FROM employees WHERE id <= 3;
# employees = Employee.objects.select('salary', condition=Condition(id__lte=3))

# SQL: SELECT salary FROM employees WHERE id >= 2 AND id <= 4;
# employees = Employee.objects.select('salary', condition=Condition(id__gte=2, id__lte=4))
# employees = Employee.objects.select('salary', condition=Condition(id__gte=2) & Condition(id__lte=4))

# SQL: SELECT salary FROM employees WHERE id < 2 OR id > 3;
# employees = Employee.objects.select('salary', condition=Condition(id__lt=2) | Condition(id__gt=3))

# SQL:
# INSERT INTO employees (first_name, last_name, salary)
#     VALUES
#        ('Yannick', 'KIKI', 1320000),
#        ('Corentin', 'ALLOH', 1560000)
# ;
# employees_data = [
#     {"first_name": "Yannick", "last_name": "KIKI", "salary": 1320000},
#     {"first_name": "Corentin", "last_name": "ALLOH", "salary": 1320000}
# ]
# Employee.objects.bulk_insert(data=employees_data)

# SQL: INSERT INTO employees (first_name, last_name, salary)
#          VALUES ('Wallis', 'KASS', 2560000)
# ;
# Employee.objects.insert(first_name="Wallis", last_name="KASS", salary=2560000)

# SQL: UPDATE employees SET salary = 3560000, age = 20 WHERE id > 4;
# Employee.objects.update(
#     new_data={'salary': 3560000, 'age': 20},
#     condition=Condition(id__gt=4)
# )

# SQL DELETE FROM employees WHERE age < 20;
# Employee.objects.delete(condition=Condition(age__lt=20))
