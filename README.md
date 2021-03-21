# yannorm

Simple ORM with Python.

## DBMS supported:
* Postgresql
* SQLite (coming soon...)
* Mysql (coming soon...)

## Demo
* [Usage template of yannorm](https://github.com/yannickkiki/yannorm-usage-template)

## Features

Overview of the features by example

```python
from yannorm import Condition, F

from .models import Employee

# SQL: SELECT * FROM employees;
employees = Employee.objects.select('*')

# SQL: SELECT id, first_name, last_name FROM employees;
Employee.objects.select('id', 'first_name', 'last_name')

# SQL: SELECT salary FROM employees WHERE id <= 3;
Employee.objects.select('salary', condition=Condition(id__lte=3))

# SQL:
# INSERT INTO employees (first_name, last_name, salary)
#     VALUES
#        ('Yannick', 'KIKI', 1320000),
#        ('Corentin', 'ALLOH', 1560000)
# ;
employees_data = [
    {"first_name": "Yannick", "last_name": "KIKI", "salary": 1320000},
    {"first_name": "Corentin", "last_name": "ALLOH", "salary": 1560000}
]
Employee.objects.bulk_insert(data=employees_data)

# SQL: INSERT INTO employees (first_name, last_name, salary)
#          VALUES ('Pythonista', 'BENINOSA', 2560000)
# ;
Employee.objects.insert(first_name="Pythonista", last_name="BENINOSA", salary=2560000)

# SQL: UPDATE employees SET salary = 3560000, age = 20 WHERE id > 4;
Employee.objects.update(
    new_data={'salary': 3560000, 'age': 20},
    condition=Condition(id__gt=4)
)

# SQL DELETE FROM employees WHERE age < 20;
Employee.objects.delete(condition=Condition(age__lt=20))

# SQL: SELECT salary FROM employees WHERE id >= 2 AND id <= 4;
Employee.objects.select('salary', condition=Condition(id__gte=2, id__lte=4))
Employee.objects.select('salary', condition=Condition(id__gte=2) & Condition(id__lte=4))

# SQL: SELECT salary FROM employees WHERE id < 2 OR id > 3;
Employee.objects.select('salary', condition=Condition(id__lt=2) | Condition(id__gt=3))

# SQL: SELECT * FROM employees WHERE first_name = last_name;
Employee.objects.select('*', condition=Condition(first_name=F('last_name')))

# SQL: SELECT * FROM employees WHERE salary < id * 60000;
Employee.objects.select('*', condition=Condition(salary__lt=F('id')*60000))

# SQL: SELECT * FROM employees WHERE id IN (3, 4);
Employee.objects.select('*', condition=Condition(id__in=[3, 4]))

# Get the list of the fields in your model 
# It corresponds to the columns of the referenced table in database
Employee.get_fields()
```

## TODO
* Review package setup
* Review code before going further 
* Add support for table/model create-alter-delete queries
* Add support for table joins
* Add `bulk_update` method to `BaseManager`
* Make a list of the ORM limitations and deduct next feature requests from that
* Create the first release of the project
