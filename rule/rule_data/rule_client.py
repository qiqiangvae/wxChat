import sqlite3


class RuleClient(object):
    connect = None
    cursor = None

    def __init__(self):
        pass

    @staticmethod
    def config():
        RuleClient.connect = sqlite3.connect('../db/weChat.db')
        RuleClient.connect.row_factory = RuleClient.__dict_factory__
        RuleClient.cursor = RuleClient.connect.cursor()

    @staticmethod
    def __dict_factory__(cursor, row):
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

    def close(self):
        RuleClient.cursor.close()
        RuleClient.connect.close()

    @staticmethod
    def new_rule(rule_data=None):
        if rule_data is None:
            return
        RuleClient.cursor.execute(
            "insert into rule ('id','rule','startTime','endTime','sort','reply') values (?,?,?,?,?,?)",
            (rule_data.get('id'), rule_data.get('rule'), rule_data.get('startTime'),
             rule_data.get('endTime'), rule_data.get('sort'), rule_data.get('reply'))
            )
        RuleClient.connect.commit()

    @staticmethod
    def query(order=None, **kwargs):
        query_sql = 'select * from rule where 1=1 '
        for k, v in kwargs:
            query_sql = query_sql + 'and %s = %s ' % (k, v)
        if order is not None:
            query_sql = query_sql + ' order by %s' % order
        RuleClient.cursor.execute(query_sql)
        return RuleClient.cursor.fetchall()


if __name__ == '__main__':
    # client.new_rule({'id': '1', 'rule': '.*', 'startTime': None, 'endTime': None, 'sort': '1'})
    RuleClient.config()
    query = RuleClient.query(order='sort')
    print(query)
