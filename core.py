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

    def select(self, *field_names, chunk_size=2000):
        fields_csv = ', '.join(field_names)
        query = f"SELECT {fields_csv} FROM {self.table_name}"

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
