from core import BaseModel, BaseManager


class EmployeeManager(BaseManager):
    table_name = "employees"


class Employee(BaseModel):
    manager_class = EmployeeManager
