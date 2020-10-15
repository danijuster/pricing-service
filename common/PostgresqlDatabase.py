import os
from typing import Dict
import psycopg2
from common.datastore import DataStore
from config import config
import json


class PostgresqlDatabase(DataStore):

    name = 'PostgresqlDatabase'

    @staticmethod
    def _create_connection() -> psycopg2:
        conn = None
        try:
            # read connection parameters
            params = config()

            # override host with environment variable instead of config ini file
            params['host'] = os.environ.get('DATABASE_URL', None)

            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params, options="-c search_path=pricing_app,dbo,public")

            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception('Could not create connection to postgresql server')

    @staticmethod
    def insert(collection: str, data: Dict):
        """Overrides DataStore.insert()"""
        # MongoDatabase.DATABASE[collection].insert(data)
        with PostgresqlDatabase._create_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("INSERT INTO " + collection + " (id, info) VALUES (%s, %s)",
                             [data['_id'], json.dumps(data)])

    @staticmethod
    def find(collection: str, query: Dict): # Add return var to cursor
        """Overrides DataStore.find()"""
        # return MongoDatabase.DATABASE[collection].find(query)
        where_statement = ''

        if len(query.keys()) > 0:
            where_statement = " WHERE info ->> '" + list(query.keys())[0] + "' = '" + list(query.values())[0] + "'"

        select_statement = "SELECT info FROM " + collection

        with PostgresqlDatabase._create_connection() as conn:
            with conn.cursor() as curs:
                curs.execute(select_statement + where_statement)
                return [x[0] for x in curs.fetchall()]

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        """Overrides DataStore.find_one()"""
        # return MongoDatabase.DATABASE[collection].find_one(query)
        with PostgresqlDatabase._create_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("SELECT info FROM " + collection +
                             " WHERE info ->> '" +
                             list(query.keys())[0] +
                             "' LIKE '" + list(query.values())[0] + "%'")
                return curs.fetchone()[0]

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        """Overrides DataStore.update()"""
        # MongoDatabase.DATABASE[collection].update(query, data, upsert=True)
        with PostgresqlDatabase._create_connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    "INSERT INTO " + collection +
                    " (id, info) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET info = %s",
                    [data['_id'], json.dumps(data), json.dumps(data)])

    @staticmethod
    def remove(collection: str, query: Dict) -> None:
        """Overrides DataStore.remove()"""
        # MongoDatabase.DATABASE[collection].remove(query)
        with PostgresqlDatabase._create_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("DELETE FROM " + collection +
                             " WHERE info ->> %s = %s", [list(query.keys())[0], list(query.values())[0]])



#PostgresqlDatabase.insert("alerts", {"_id": "a1111111", "name": "dani", "age": 45})

#PostgresqlDatabase.remove("alerts", {"_id": "a1111111"})

# PostgresqlDatabase.update("alerts",
#                           {"id": "a1111111"},
#                           {"_id": "a1111111", "name": "dani", "age": 45})

#a = PostgresqlDatabase.find_one('alerts', {"_id": "a1111111"})

#print([x for x in a])

