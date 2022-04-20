import records
import re
from babel.numbers import parse_decimal, NumberFormatError


schema_re = re.compile(r"\((.+)\)")
num_re = re.compile(r"[-+]?\d*\.\d+|\d+")

agg_ops = ["", "MAX", "MIN", "COUNT", "SUM", "AVG"]
cond_ops = ["=", ">", "<", "OP"]


class DBEngine:
    def __init__(self, fdb):
        # fdb = 'data/test.db'
        self.db = records.Database("sqlite:///{}".format(fdb))

    def execute_query(self, table_id, query, *args, **kwargs):
        return self.execute(
            table_id,
            query.sel_index,
            query.agg_index,
            query.conditions,
            *args,
            **kwargs
        )

    def execute(
        self, table_id, select_index, aggregation_index, conditions, lower=True
    ):
        if not table_id.startswith("table"):
            table_id = "table_{}".format(table_id.replace("-", "_"))
        table_info = (
            self.db.query(
                "SELECT sql from sqlite_master WHERE tbl_name = :name", name=table_id
            )
            .all()[0]
            .sql.replace("\n", "")
        )
        schema_str = schema_re.findall(table_info)[0]
        schema = {}
        for tup in schema_str.split(", "):
            c, t = tup.split()
            schema[c] = t
        select = "col{}".format(select_index)
        agg = agg_ops[aggregation_index]
        if agg:
            select = "{}({})".format(agg, select)
        where_clause = []
        where_map = {}
        for col_index, op, val in conditions:
            if lower and (isinstance(val, str) or isinstance(val, str)):
                val = val.lower()
            if schema["col{}".format(col_index)] == "real" and not isinstance(
                val, (int, float)
            ):
                try:
                    val = float(parse_decimal(val))
                except NumberFormatError as e:
                    val = float(num_re.findall(val)[0])
            where_clause.append(
                "col{} {} :col{}".format(col_index, cond_ops[op], col_index)
            )
            where_map["col{}".format(col_index)] = val
        where_str = ""
        if where_clause:
            where_str = "WHERE " + " AND ".join(where_clause)
        query = "SELECT {} AS result FROM {} {}".format(select, table_id, where_str)
        # print query
        out = self.db.query(query, **where_map)
        return [o.result for o in out]
