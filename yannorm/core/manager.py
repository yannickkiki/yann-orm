import itertools
import importlib

import psycopg2


class BaseManager:
    connection = None
    table_name = ""

    @classmethod
    def set_connection(cls, **database_settings):
        connection = psycopg2.connect(**database_settings)
        connection.autocommit = True
        cls.connection = connection

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, chunk_size=2000, condition=None):
        # Build SELECT query
        query = f"SELECT {', '.join(field_names)} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition.str}"

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)

        # Fetch data obtained with the previous query execution and transform it into `model_class` objects.
        # The fetching is done by batches to avoid to run out of memory.
        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            rows = cursor.fetchmany(size=chunk_size)
            for row in rows:
                data = dict()
                for idx, field_name in enumerate(field_names):
                    value = row[idx]
                    data.update({field_name: value})
                model_objects.append(self.model_class(**data))
            is_fetching_completed = len(rows) < chunk_size

        return model_objects

    def bulk_insert(self, data):
        # Get fields to insert [fx, fy, fz] and set values in this format [(x1, y1, z1), (x2, y2, z2), ... ] to
        # facilitate the INSERT query building
        field_names = data[0].keys()
        values = list()
        for row in data:
            assert row.keys() == field_names
            values.append(tuple(row[field_name] for field_name in field_names))

        # Build INSERT query and params following documentation at
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        # values_format example with 3 rows to insert with 2 fields: (%s, %s), (%s, %s), (%s, %s)
        n_fields, n_rows = len(field_names), len(values)
        values_row_format = f'({", ".join(["%s"]*n_fields)})'
        values_format = ", ".join([values_row_format]*n_rows)

        query = f"INSERT INTO {self.table_name} ({', '.join(field_names)}) VALUES {values_format}"
        params = tuple(itertools.chain(*values))

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query, params)

    def insert(self, **row_data):
        self.bulk_insert(data=[row_data])

    def update(self, new_data, condition=None):
        # Build UPDATE query
        query = f"UPDATE {self.table_name} " \
                f"SET {', '.join([f'{field_name} = {value}' for field_name, value in new_data.items()])}"
        if condition:
            query += f" WHERE {condition.str}"

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)

    def delete(self, condition=None):
        # Build DELETE query
        query = f"DELETE FROM {self.table_name} "
        if condition:
            query += f" WHERE {condition.str}"

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)


settings_module = importlib.import_module("settings")
db_settings = getattr(settings_module, "DB_SETTINGS")
BaseManager.set_connection(**db_settings)
