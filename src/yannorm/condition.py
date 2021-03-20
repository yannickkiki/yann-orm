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
