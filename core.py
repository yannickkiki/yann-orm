import psycopg2

CREDENTIALS_DB = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'pgtest',
    'user': 'yannick',
    'password': 'yannick'
}


class Manager:
    table_name = ""

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, chunk_size=2000, condition=None):
        fields_csv = ', '.join(field_names)
        query = f"SELECT {fields_csv} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition.str}"

        connection = psycopg2.connect(**CREDENTIALS_DB)
        cursor = connection.cursor()
        cursor.execute(query)

        result = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            rows = cursor.fetchmany(size=chunk_size)
            for row in rows:
                data = dict()
                for idx, field_name in enumerate(field_names):
                    value = row[idx]
                    data.update({field_name: value})
                result.append(self.model_class(**data))
            is_fetching_completed = len(rows) < chunk_size
        return result


class ModelMeta(type):
    manager_class = Manager

    @property
    def objects(cls):
        return cls.manager_class(model_class=cls)


class Model(metaclass=ModelMeta):

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        return str(self.__dict__)


class Condition:
    operations_map = {
        'eq': '=',
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>='
    }

    def __init__(self, **kwargs):
        parts = list()
        for expr, value in kwargs.items():
            if '__' not in expr:
                expr += '__eq'
            field, operation_expr = expr.split('__')
            operation_str = self.operations_map[operation_expr]
            parts.append(f'{field} {operation_str} {value}')
        self.str = ' AND '.join(parts)

    def __or__(self, other):
        return self._merge_with(other_condition=other, logical_operator='OR')

    def __and__(self, other):
        return self._merge_with(other_condition=other, logical_operator='AND')

    def _merge_with(self, other_condition, logical_operator='AND'):
        condition_resulting = Condition()
        condition_resulting.str = f"({self.str}) {logical_operator} ({other_condition.str})"
        return condition_resulting
