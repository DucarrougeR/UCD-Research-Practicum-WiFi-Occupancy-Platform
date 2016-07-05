class QueryBuilder:

    def __init__(self):
        self._action = 'SELECT'
        self._joins = []
        self._table = ''
        self._action_fields = []
        self._params = ''
        self._wheres = []
        self._or_wheres = []
        self._operators = ['=',
         '<',
         '>',
         '<=',
         '>=',
         '!=']
        self._params_count = 0
        self._limit = None
        self._query = ''
        self._order_by = None
        self._order_direction = 'DESC'
        self._group_by = None
        self._results = []
        self._count = 0
        self._error = []

    def _valid_operator(self, op):
        if op in self._operators:
            return True
        return False

    def select(self, table, fields = []):
        if len(fields) > 0:
            self._action_fields = fields
        self._action = 'SELECT'
        self._table = table
        return self

    def insert(self, table, fields = [], values = []):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def where(self, column = '', op = '', value = ''):
        if not self._valid_operator(op):
            raise ValueError('Operator given is not valid')
        self._wheres.append([column, op, str(value)])
        return self

    def or_where(self, column = '', op = '', value = ''):
        if not self._valid_operator(op):
            raise ValueError('Operator given is not valid')
        self._or_wheres.append([column, op, str(value)])
        return self

    def join(self, table, table_val_1, op, table_val_2):
        if self._action != 'SELECT':
            raise ValueError('Cannot perform a join on ' + self._action)
        if not self._valid_operator(op):
            raise ValueError(op + ' is not a valid operator')
        self._joins.append([table,
         table_val_1,
         op,
         table_val_2])
        return self

    def query(self):
        sql = ''
        if self._action == 'SELECT':
            if len(self._action_fields) > 0:
                field_string = ','.join(self._action_fields)
            else:
                field_string = '*'
            sql += self._action + ' ' + field_string + ' FROM ' + self._table
            if len(self._joins) > 0:
                join_string = ''
                for join in self._joins:
                    join_string += ' JOIN ' + join[0] + ' ON ' + join[1] + ' ' + join[2] + ' ' + join[3]

                sql += join_string
            if self._group_by:
                sql += ' GROUP BY ' + self._group_by
            if self._order_by:
                sql += ' ORDER BY ' + self._order_by + ' ' + self._order_direction
            if self._limit:
                sql += ' LIMIT ' + self._limit
        if self._action != 'INSERT':
            and_where_string = ''
            or_where_string = ''
            if len(self._wheres) > 0:
                where_list = []
                for where in self._wheres:
                    where_list.append(' '.join(where))

                and_where_string = ' AND '.join(where_list)
            if len(self._or_wheres) > 0:
                where_list = []
                for where in self._wheres:
                    where_list.append(' '.join(where))

                or_where_string = ' OR '.join(where_list)
            if len(and_where_string):
                sql += ' WHERE ' + and_where_string
            if len(or_where_string):
                sql += ' OR ' + or_where_string
        self._query = sql
        return self

    def get_query(self):
        if not self._query:
            self.query()
        return self._query