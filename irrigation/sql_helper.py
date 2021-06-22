import mariadb
import yaml
import os


with open(os.path.join(os.path.dirname(__file__), r'../.db_user')) as file:
    db_user = yaml.load(file, Loader=yaml.FullLoader)


def get_conn(database='irrigation'):
    return mariadb.connect(
      host="localhost",
      user=db_user['username'],
      password=db_user['password'],
      database=database
    )


def create_table_sql(name, columns, replace=False):
    sql = 'CREATE OR REPLACE TABLE' if replace else 'CREATE TABLE IF NOT EXISTS'
    sql += f' {name} ('
    sql += ', '.join([f"{col['name']} {col['type']}" for col in columns])
    sql += ')'
    
    return sql


class my_dao:
    def get_list(self, where_clause=None, values=[]):
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLENAME} {where_clause}", values)

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

                return rows


class Schema:
    def setup(self, replace=False):
        with get_conn(database=None) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS irrigation")

        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_table_sql('zones'
                                                , [
                                                    {'name': 'id', 'type': 'INT NOT NULL'}
                                                    , {'name': 'name', 'type': 'VARCHAR(128)'}
                                                    , {'name': 'disabled', 'type': 'BOOLEAN DEFAULT TRUE'}
                                                    , {'name': 'interval_days', 'type': 'INT'}
                                                    , {'name': 'scheduled_time', 'type': 'TIMESTAMP'}
                                                    , {'name': 'duration_minutes', 'type': 'INT'}]
                                                , replace))
                if replace:
                    cursor.executemany("INSERT INTO zones (id) VALUES (?)", [(1,), (2,), (3,), (4,), (5,), (6,)])
                    conn.commit()

                cursor.execute(create_table_sql('temperature'
                                                , [
                                                    {'name': 'ts', 'type': 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP'}
                                                    , {'name': 'temp', 'type': 'FLOAT'}]
                                                , replace))

                cursor.execute(create_table_sql('water'
                                                , [
                                                    {'name': 'zone', 'type': 'INT'}
                                                    , {'name': 'alias', 'type': 'VARCHAR(128)'}
                                                    , {'name': 'start_ts', 'type': 'TIMESTAMP NOT NULL'}
                                                    , {'name': 'end_ts', 'type': 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP'}
                                                    , {'name': 'gallons', 'type': 'FLOAT'}]
                                                , replace))

                cursor.execute(create_table_sql('moisture'
                                                , [
                                                    {'name': 'ts', 'type': 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP'}
                                                    , {'name': 'a0', 'type': 'FLOAT'}
                                                    , {'name': 'a1', 'type': 'FLOAT'}
                                                    , {'name': 'a2', 'type': 'FLOAT'}
                                                    , {'name': 'a3', 'type': 'FLOAT'}]
                                                , replace))


class Zone(my_dao):
    TABLENAME = "zones"

    def update(self, zone, name=None, disabled=False, interval_days=None, scheduled_time=None, duration_minutes=None):
        query = f"UPDATE {self.TABLENAME} SET "
        values = ()

        if name:
            query += f'name = ?, '
            values += (name,)
        if disabled:
            query += f'disabled = ?, '
            values += (disabled,)
        if interval_days:
            query += f'interval_days = ?, '
            values += (interval_days,)
        if scheduled_time:
            query += f'scheduled_time = ?, '
            values += (scheduled_time,)
        if duration_minutes:
            query += f'duration_minutes = ?, '
            values += (duration_minutes,)

        query = query[:-2]  # remove trailing comma
        query += "WHERE id = ?"
        values += (zone,)

        print(query)

        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()


def insert_temperature(temp):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO temperature (temp) VALUES (?)", (temp,))
            conn.commit()


def insert_moistures(a0, a1, a2, a3):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO moisture (a0, a1, a2, a3) VALUES (?, ?, ?, ?)", (a0, a1, a2, a3))
            conn.commit()


class Water(my_dao):
    TABLENAME = "water"

    # Todo, make into a real DAO...
    def insert(self, zone, alias, start_ts, gallons):
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"INSERT INTO {self.TABLENAME} (zone, alias, start_ts, gallons) VALUES (?, ?, ?, ?)", (zone, alias, start_ts, gallons))
                conn.commit()
