import os
import mysql.connector
from mysql.connector import errorcode
import bot_logic


config = {
  'user': 'root',
  'password': 'Monkey321',
  'host': '127.0.0.1',
  'database': 'photo_editor',
  'raise_on_warnings': True
}


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passsword=user_password,
            database='photo_editor',
            raise_on_warnings=True
        )
        print('Connection to MySQL DB successful')
    except errorcode as e:
        print(f'The error "{e}" occurred')
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query executed successful')
    except errorcode as e:
        print(f'The error "{e}" occurred')


add_user_query = """
INSERT INTO user_photo (user) VALUES (%s)
"""

add_content_query = """
INSERT INTO user_photo (path_to_photo) VALUES (%s)
"""

add_style_query = """
INSERT INTO user_photo (path_to_style) VALUES (%s)
"""
