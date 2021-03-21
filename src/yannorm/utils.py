class F:
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

    def __init__(self, field_name=None):
        self.sql_format = field_name
        
    def __add__(self, other):
        return self._combine(other, operator=self.ADD)

    def __radd__(self, other):
        return self._combine(other, operator=self.ADD, is_reversed=True)

    def __sub__(self, other):
        return self._combine(other, operator=self.SUB)

    def __rsub__(self, other):
        return self._combine(other, operator=self.SUB, is_reversed=True)

    def __mul__(self, other):
        return self._combine(other, operator=self.MUL)

    def __rmul__(self, other):
        return self._combine(other, operator=self.MUL, is_reversed=True)

    def __truediv__(self, other):
        return self._combine(other, operator=self.DIV)

    def __rtruediv__(self, other):
        return self._combine(other, operator=self.DIV, is_reversed=True)

    def _combine(self, other, operator, is_reversed=False):
        f_obj = F()
        part_left = self.sql_format
        part_right = other.sql_format if isinstance(other, F) else other
        if is_reversed:
            part_left, part_right = part_right, part_left
        f_obj.sql_format = f'{part_left} {operator} {part_right}'
        return f_obj


class Condition:
    operations_map = {
        'eq': '=',
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>=',
        'in': 'IN'
    }

    def __init__(self, **kwargs):
        sql_format_parts = list()
        self.query_vars = list()
        for expr, value in kwargs.items():
            if '__' not in expr:
                expr += '__eq'
            field, operation_expr = expr.split('__')
            operation_str = self.operations_map[operation_expr]

            if isinstance(value, F):
                f_obj = value
                sql_format_parts.append(f'{field} {operation_str} {f_obj.sql_format}')
            elif isinstance(value, list):
                vars_list = value
                sql_format_parts.append(f'{field} {operation_str} ({", ".join(["%s"]*len(vars_list))})')
                self.query_vars += vars_list
            else:
                sql_format_parts.append(f'{field} {operation_str} %s')
                self.query_vars.append(value)
        self.sql_format = ' AND '.join(sql_format_parts)

    def __or__(self, other):
        return self._merge_with(other, logical_operator='OR')

    def __and__(self, other):
        return self._merge_with(other, logical_operator='AND')

    def _merge_with(self, other, logical_operator='AND'):
        condition_resulting = Condition()
        condition_resulting.sql_format = f"({self.sql_format}) {logical_operator} ({other.sql_format})"
        condition_resulting.query_vars = self.query_vars + other.query_vars
        return condition_resulting


class Field:
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} ({self.data_type})>"
