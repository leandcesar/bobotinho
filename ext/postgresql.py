# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Adapted from: https://github.com/cjauvin/little_pger/blob/20ca16c42352377f46615f216b7dde235c7bfad4/little_pger.py

import asyncpg
import collections

reserved_pg_keywords = (
    "all", "analyse", "analyze", "and", "any", "array", "as", "asc", "asymmetric",
    "authorization", "binary", "both", "case", "cast", "check", "collate", "collation",
    "column", "concurrently", "constraint", "create", "cross", "current_catalog",
    "current_date", "current_role", "current_schema", "current_time", "current_timestamp",
    "current_user", "default", "deferrable", "desc", "distinct", "do", "else", "end",
    "except", "false", "fetch", "for", "foreign", "freeze", "from", "full", "grant",
    "group", "having", "ilike", "in", "initially", "inner", "intersect", "into",
    "is", "isnull", "join", "lateral", "leading", "left", "like", "limit", "localtime",
    "localtimestamp", "natural", "not", "notnull", "null", "offset", "on", "only",
    "or", "order", "outer", "overlaps", "placing", "primary", "references", "returning",
    "right", "select", "session_user", "similar", "some", "symmetric", "table",
    "tablesample", "then", "to", "trailing", "true", "union", "unique", "user", "using",
    "variadic", "verbose", "when", "where", "window", "with",
)


def _check_args(func_name, args, allowed_args):
    if not set(args) <= set(allowed_args):
        raise TypeError(f"Unexpected keyword argument(s) in {func_name}: {list(set(args) - set(allowed_args))}")
    return True


def _flatten(values: list):
    flat_values = []
    for value in values:
        if isinstance(value, set):
            flat_values += list(value)
        else:
            flat_values.append(value)
    return flat_values


def _inc_or_dec(field: str, value):
    if isinstance(value, str):
        value = value.replace(" ", "")
        return (
            value.startswith((field + "+", field + "-"))
            and value[len(field)+1:].isdigit()
        )


def _pg_syntax(query: str):
    for n in range(1, query.count("%s") + 1):
        query = query.replace("%s", f"${n}", 1)
    return query


def _get_where_clause_comp_item(c, v):
    # Returns a triple: (field, comp_operator, value placeholder)
    if isinstance(c, tuple):
        assert len(c) in [2, 3]
        if len(c) == 2:
            # (field, comp_operator, value placeholder)
            return c + ("%s",)
        elif len(c) == 3:
            # (field, comp_operator, transformed value placeholder)
            return (f"{c[2]}({c[0]})", c[1], f"{c[2]}(%s)")
    elif isinstance(v, tuple):
        return (c, "in", "%s")
    return (c, "=", "%s")


def _get_where_clause(items, type_: str = "and"):
    wc = []
    for c, v in items:
        if c == "exists":
            wc.append(f"exists ({v})")
        elif isinstance(v, set):
            sub_wc = " and ".join(["%s %s %s" % _get_where_clause_comp_item(c, vv) for vv in v])
            wc.append(f"({sub_wc})")
        else:
            wc.append("%s %s %s" % _get_where_clause_comp_item(c, v))
    return (f" {type_} ").join(wc)


class PostgreSQL(object):
    def __init__(self):
        pass

    def __del__(self):
        try:
            self.pool.terminate()
        except AttributeError:
            pass
        except Exception as err:
            raise err        
    
    @classmethod
    async def init(self, dsn, loop=None):
        self = PostgreSQL()
        self.dsn = dsn
        self.loop = loop
        self.pool = await asyncpg.create_pool(
            dsn, loop=loop, max_inactive_connection_lifetime=0, min_size=1, max_size=10
        )
        return self
    
    async def _exec_query(self, method: str, query: str, qvalues=[]):
        # Acquire a database connection from the pool.
        async with self.pool.acquire() as conn:
            # Create a Transaction object.
            async with conn.transaction():
                # Execute an SQL command (or commands).
                if not qvalues:
                    res = await getattr(conn, method)(_pg_syntax(query))
                else:
                    res = await getattr(conn, method)(_pg_syntax(query), *_flatten(qvalues))
            # Release a database connection back to the pool.
            await self.pool.release(conn)
        return res

    async def select(self, table, **kwargs):
        """SQL select statement helper.
        Optional kwargs:
            what -- projection items (str, list or dict, default '*')
                ex1: what='color' --> "select color from .."
                ex2: what=['color', 'name'] --> "select color, name from .."
                ex3: what='max(price)' --> "select max(price) from .."
                ex4: what={'*':True, 'price is null':'is_price_valid'} 
                    --> "select *, price is null as is_price_valid from .."
                ex5: what=['age', 'count(*)'], group_by='age'
                     --> "select age, count(*) from .. group by age"
            [inner_]join -- either: table `str` or (table, field) `tuple`, (or list of those)
            left_join -- similar to join
            right_join -- similar to join
            where -- AND-joined where clause dict (default empty)
            where_or -- OR-joined where clause dict (default empty)
            group_by -- group by clause (str or list, default None)
            order_by -- order by clause (str or list, default None)
            limit -- limit clause (default None)
            offset -- offset clause (default None)
            rows -- all, row or val (default 'row')
            get_count -- wrap the entire query inside a select count(*) outer query (default False)
        """
        _check_args("select", kwargs.keys(), ("what", "join", "inner_join", "left_join", 
            "right_join", "where", "where_or", "order_by", "group_by", "limit", "offset", 
            "rows", "get_count"))
        rows = kwargs.pop("rows", "row")
        if rows not in ("all", "row", "val"):
            raise ValueError(f"Expected `all`, `row` or `val` in `rows` arg, not `{rows}`")
        what = kwargs.pop("what", "*")
        inner_join = kwargs.pop("join", kwargs.pop("inner_join", {}))
        left_join = kwargs.pop("left_join", {})
        right_join = kwargs.pop("right_join", {})
        where = kwargs.pop("where", {}).copy()  # need a copy because we might pop an 'exists' item
        where_or = kwargs.pop("where_or", {}).copy()  # idem
        order_by = kwargs.pop("order_by", None)
        group_by = kwargs.pop("group_by", None)
        limit = kwargs.pop("limit", None)
        offset = kwargs.pop("offset", None)
        get_count = kwargs.pop("get_count", False)

        proj_items = []
        if what:
            if isinstance(what, dict):
                proj_items = ["{}{}".format(w, f" as {n}" if isinstance(n, str) else "") for w, n in what.items()]
            elif isinstance(what, str):
                proj_items = [what]
            else:
                proj_items = list(what)
        proj = ", ".join(proj_items)
        q = f"select {proj} from {table} "
        
        jj = [(inner_join, "inner"), (left_join, "left"), (right_join, "right")]
        for join_elem, join_type in jj:
            if not join_elem:
                continue
            for e in join_elem if isinstance(join_elem, list) else [join_elem]:
                if isinstance(e, str):
                    #pkey = self.get_table_infos(e.split()[0]).pkey
                    #q += f" {join_type} join {e} using ({pkey})"
                    pass
                elif isinstance(e, tuple):
                    if len(e) == 2:
                        t, f = e
                        q += f" {join_type} join {t} using ({f})"
                    else:
                        raise TypeError(f"Expected `table_as_str`, a (table_as_str, field_as_str) tuple, or a list of those; not `{type(e).__name__}`")
                else:
                    raise TypeError(f"Expected `table_as_str`, a (table_as_str, field_as_str) tuple, or a list of those; not `{type(e).__name__}`")

        q += " where true "
        if where:
            where_clause = _get_where_clause(where.items())
            q += f" and {where_clause}"
            where.pop("exists", None)
        if where_or:
            where_or_clause = _get_where_clause(where_or.items(), "or")
            q += f" and ({where_or_clause})"
            where_or.pop("exists", None)
        if group_by:
            if isinstance(group_by, str):
                q += f" group by {group_by}"
            else:
                q += " group by {}".format(", ".join([e for e in group_by]))
        if order_by:
            if isinstance(order_by, str):
                q += f" order by {order_by}"
            else:
                q += " order by {}".format(", ".join([e for e in order_by]))
        if limit:
            q += f" limit {limit}"
        if offset:
            q += f" offset {offset}"
        if get_count:
            q = f"select count(*) from ({q}) _"
            rows = "row"
        
        if rows == "all":
            # Run a query and return the results as a list of Record.
            return await self._exec_query("fetch", q, list(where.values()) + list(where_or.values()), **kwargs)
        elif rows == "row":
            # Run a query and return the first row as a Record instance, 
            # or None if no records were returned by the query.
            return await self._exec_query("fetchrow", q, list(where.values()) + list(where_or.values()), **kwargs)
        elif rows == "val":
            # Run a query and return a value in the first record, 
            # or None if no records were returned by the query.
            return await self._exec_query("fetchval", q, list(where.values()) + list(where_or.values()), **kwargs)

    async def select1(self, table, **kwargs):
        """SQL select statement helper (syntactic sugar for value select call).
        """
        _check_args("select1", kwargs.keys(), ("what", "join", "inner_join", "left_join", 
            "right_join", "where", "where_or", "order_by", "group_by", "limit", "offset"))
        return await self.select(table, rows="val", **kwargs)

    async def select_all(self, table, **kwargs):
        """SQL select statement helper (syntactic sugar for all rows select call).
        """
        _check_args("select_all", kwargs.keys(), ("what", "join", "inner_join", "left_join", 
            "right_join", "where", "where_or", "order_by", "group_by", "limit", "offset"))
        return await self.select(table, rows="all", **kwargs)

    async def insert(self, table, **kwargs):
        """SQL insert statement helper.
        Optional kwargs:
            values -- dict with values to set (default empty)
            map_values -- dict containing a mapping to be performed on 'values'
                        (e.g. {'': None}, to convert empty strings to nulls)
        """
        _check_args("insert", kwargs.keys(), ("values", "map_values"))
        values = kwargs.pop("values", {})
        if not values:
            q = f"insert into {table} default values returning *"
        else:
            map_values = kwargs.pop("map_values", {})
            values =  {
                k: (map_values.get(v, v) if isinstance(v, collections.Hashable) else v)
                for k, v in values.items()
            }
            fields = ",".join(values.keys())
            vals = ",".join("%s" for v in values)
            q = f"insert into {table} ({fields}) values ({vals}) returning *"

        await self._exec_query("execute", q, values.values(), **kwargs)

    async def update(self, table, **kwargs):
        """SQL update statement helper.
        Optional kwargs:
            set|values -- dict with values to set (either keyword works; default empty)
            where -- AND-joined where clause dict (default empty)
            where_or -- OR-joined where clause dict (default empty)
            map_values -- dict containing a mapping to be performed on 'values'
                        (e.g. {'': None}, to convert empty strings to nulls)
        """
        _check_args("update", kwargs.keys(), ("set", "values", "where", "where_or", "map_values"))
        values = kwargs.pop("values", kwargs.pop("set", {}))
        where = kwargs.pop("where", {})
        where_or = kwargs.pop("where_or", {})
        map_values = kwargs.pop("map_values", {})
        values = {
            k: (map_values.get(v, v) if isinstance(v, collections.Hashable) else v)
            for k, v in values.items()
        }
        q = f"update {table} set "
        q += ", ".join([f"{k}={v}" if _inc_or_dec(k, v) else f"{k}=%s" for k, v in values.items()])
        values = {k: v for k, v in values.items() if not _inc_or_dec(k, v)}
        if where:
            where_clause = _get_where_clause(where.items())
            q += f" where {where_clause}"
        if where_or:
            where_or_clause = _get_where_clause(where_or.items(), "or")
            if where:
                q += f" and ({where_or_clause})"
            else:
                q += f" where {where_or_clause}"
        vals = list(values.values()) + list(where.values()) + list(where_or.values())
        await self._exec_query("execute", q, vals, **kwargs)

    async def upsert(self, table, pkey="id", **kwargs):
        """SQL insert/update statement helper.
        Optional kwargs:
            set|values -- dict with values to set (either keyword works; default empty)
            map_values -- dict containing a mapping to be performed on 'values'
                        (e.g. {'': None}, to convert empty strings to nulls)
        """
        _check_args("upsert", kwargs.keys(), ("set", "values", "map_values"))
        values = kwargs.pop("values", kwargs.pop("set", {}))
        if not values:
            q = f"insert into {table} default values"
        else:
            map_values = kwargs.pop("map_values", {})
            H = collections.Hashable
            values = {
                k: map_values.get(v, v) if isinstance(v, H) else v
                for k, v in values.items()
            }
            fields = ",".join(values.keys())
            vals = ",".join(["%s" for _ in values])
            updates = ",".join([f"{c} = excluded.{c}" for c in values.keys()])
            q = (
                f"insert into {table} ({fields}) values ({vals}) "
                f"on conflict ({pkey}) do update set {updates}"
            )

        await self._exec_query("execute", q, values.values(), **kwargs)

    async def delete(self, table, **kwargs):
        """SQL delete statement helper.
        Optional kwargs:
            where -- AND-joined where clause dict (default empty)
            where_or -- OR-joined where clause dict (default empty)
        """
        _check_args("delete", kwargs.keys(), ("where", "where_or", "tighten_sequence"))
        where = kwargs.pop("where", {})
        where_or = kwargs.pop("where_or", {})
        q = f"delete from {table}"
        if where:
            where_clause = _get_where_clause(where.items())
            q += f" where {where_clause}"
        if where_or:
            where_or_clause = _get_where_clause(where_or.items(), "or")
            if where:
                q += f" and ({where_or_clause})" 
            else:
                q += f" where {where_or_clause}"
        await self._exec_query("execute", q, list(where.values()) + list(where_or.values()), **kwargs)

    async def count(self, table, **kwargs):
        """SQL select count statement helper.
        Optional kwargs:
            [inner_]join -- either: table `str` or (table, field) `tuple`, (or list of those)
            left_join -- similar to join
            right_join -- similar to join
            left_join -- .. (default empty)
            where -- AND-joined where clause dict (default empty)
            where_or -- OR-joined where clause dict (default empty)
            group_by -- group by clause (str or list, default None)
        """
        _check_args("count", kwargs.keys(), ("what", "join", "inner_join", "left_join", 
            "right_join", "where", "where_or", "group_by"))
        if kwargs.get("group_by", None) is None:
            _ = kwargs.pop("what", None)
            row = await self.select(table, what="count(*)", rows="row", **kwargs)
        else:
            row = await self.select(table, get_count=True, **kwargs)
        return int(row["count"])

    async def exists(self, table, **kwargs):
        """Check whether at least one record exists.
        Optional kwargs:
            what -- projection items (str, list or dict, default '*')
            where -- AND-joined where clause dict (default empty)
            where_or -- OR-joined where clause dict (default empty)
        """
        _check_args("exists", kwargs.keys(), ("what", "where", "where_or"))
        return await self.select(table, limit=1, rows="row", **kwargs) is not None

    async def get_pkey_column(self, table):
        return (
            await self._exec_query(
                "fetchrow", 
                """
                select pg_attribute.attname as pkey_name
                from pg_index, pg_class, pg_attribute
                where
                pg_class.oid = %s::regclass and indrelid = pg_class.oid and
                pg_attribute.attrelid = pg_class.oid and
                pg_attribute.attnum = any(pg_index.indkey) and indisprimary;
                """,
                [table],
            ) or {}
        ).get("pkey_name")

    async def get_pkey_sequence(self, table):
        return (
            await self._exec_query(
                "fetchrow", 
                """
                select pg_get_serial_sequence(%s, a.attname) seq_name
                from pg_index i, pg_class c, pg_attribute a
                where
                c.oid = %s::regclass and indrelid = c.oid and
                a.attrelid = c.oid and a.attnum = any(i.indkey) and indisprimary;
                """,
                [table, table],
            ) or {}
        ).get("seq_name")

    async def sql(self, method, q, qvals=None):
        return await self._exec_query(method, q, qvals)
