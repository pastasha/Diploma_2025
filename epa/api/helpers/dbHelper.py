from configparser import ConfigParser
from typing import Dict
from uuid import uuid4
import pandas as pd
import shutil
import psycopg2
from typing import Dict, List
import psycopg2.extras as psql_extras
from datetime import datetime, timedelta
import os


ALLOWED_EXTENSIONS = {"csv", "xml"}
SESSION_DAYS = 7
SESSION_MAX_AGE = SESSION_DAYS * 24 * 60 * 60
USER_TABLE = "customer"
ALL_USER_VALUES_QUERY = "SELECT * from " + USER_TABLE + ";"
DATA_FILE_NAME = "/data.csv"

# Generate a new user ID
def generate_user_id():
    return str(uuid4())

# Allowed file extension check
def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_user_static_folder(user_id):
    try:
        folder_path = 'static/images/' + user_id + '/plots'
        shutil.rmtree(folder_path)
        print('Static folder of current user is removed. User ID: ' + user_id)
    except:
        print('Static folder not deleted. User ID: ' + user_id)

def load_connection_info(
        ini_filename: str
    ) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info


def get_column_names(
        table: str,
        cur: psycopg2.extensions.cursor
    ) -> List[str]:
    cur.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
    col_names = [result[0] for result in cur.fetchall()]
    return col_names


def get_data_from_db(
        query: str,
        conn: psycopg2.extensions.connection,
        cur: psycopg2.extensions.cursor,
        df: pd.DataFrame,
        col_names: List[str]
    ) -> pd.DataFrame:
    try:
        response = []
        cur.execute(query)
        while True:
            # Fetch the next 100 rows
            query_results = cur.fetchmany(100)
            # If an empty list is returned, then we've reached the end of the results
            if query_results == list():
                break

            # Create a list of dictionaries where each dictionary represents a single row
            results_mapped = [
                {col_names[i]: row[i] for i in range(len(col_names))}
                for row in query_results
            ]

            # Append the fetched rows to the DataFrame
            response.append(results_mapped)
        return response
    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()
    try:
        # Execute the table creation query
        cur.execute(query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()

def insert_data(
        query: str,
        conn: psycopg2.extensions.connection,
        cur: psycopg2.extensions.cursor,
        df: pd.DataFrame,
        page_size: int
    ) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]
    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)
    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()
    else:
        conn.commit()

def upsert_customer_to_db(
        user_id: str,
        instance_path: str,
        conn: psycopg2.extensions.connection,
        cur: psycopg2.extensions.cursor,
    ) -> None:
    try:
        files_path = instance_path + '/' + user_id,
        session_exp = datetime.now() + timedelta(days=SESSION_DAYS)
        # Construct the SQL statement with placeholders
        insert_statement = "INSERT INTO " + USER_TABLE + "(id, user_id, files_path, session_exp) VALUES (DEFAULT, %s, %s, %s)"
        # Execute the SQL statement with the values
        cur.execute(insert_statement, (user_id, files_path, session_exp))
    except Exception as error:
        print(f"-{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()
    else:
        conn.commit()

def getCustomerData(customer_folder):
    try:
        data_path = customer_folder + DATA_FILE_NAME
        data = os.path.abspath(data_path)
        dataframe = pd.read_csv(data)
        return dataframe
    except Exception as error:
        print("- getCustomerData error:")
        print(f"- {type(error).__name__}: {error}")