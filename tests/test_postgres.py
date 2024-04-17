import unittest
import psycopg2

class TestLogin(unittest.TestCase):

    def setUp(self):
        dbname="mydatabase"  
        user="postgres"   
        password="admin"     
        host="localhost"     

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

    def test_postgres_connection(self):
        '''Check if the connection to the PostgreSQL server is successful.'''
        
        self.assertIsNotNone(self.conn)