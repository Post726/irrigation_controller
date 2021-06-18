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
                                                {'name': 'start_ts', 'type': 'TIMESTAMP NOT NULL'}
                                                , {'name': 'end_ts', 'type': 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP'}
                                                , {'name': 'gallons', 'type': 'FLOAT'}]
                                            , replace))


def insert_temperature(temp):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO temperature (temp) VALUES (?)", (temp,))
            conn.commit()


def insert_water(start_ts, gallons):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO water (start_ts, gallons) VALUES (?, ?)", (start_ts, gallons))
            conn.commit()


def get_temperatures():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM temperature ORDER BY ts")
            
            return [{'ts': ts, 'temperature': temp} for (ts, temp) in cursor]


def get_water():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM water ORDER BY start_ts")
            
            return [{'start_ts': start_ts, 'end_ts': end_ts, 'gallons': gallons} for (start_ts, end_ts, gallons) in cursor]

# setup(replace=True)
# insert_water('2020-01-01 00:00:00', 5)
# insert_temperature(56)
# insert_temperature(57)
# print(get_temperatures())
# print(get_water())