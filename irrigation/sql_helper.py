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


def setup(replace=False):
    with get_conn(database=None) as conn:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS irrigation")
            
    with get_conn() as conn:
        with conn.cursor() as cursor:
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


def insert_water(zone, alias, start_ts, gallons):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO water (zone, alias, start_ts, gallons) VALUES (?, ?)", (zone, alias, start_ts, gallons))
            conn.commit()


def get_list(table):
    if table not in ['water', 'temperature', 'moisture']:
        raise ValueError(f'{table} is not a known table!')

    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")

            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return rows

# setup(replace=True)
# insert_water('2020-01-01 00:00:00', 5)
# insert_temperature(56)
# insert_temperature(57)
# print(get_temperatures())
# print(get_water())