from core import Model, Manager


class EmployeeManager(Manager):
    table_name = "employees"


class Employee(Model):
    manager_class = EmployeeManager
