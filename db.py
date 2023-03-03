import pymysql
from pymysql.cursors import DictCursor

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="031002",
    db="test_db1",
    cursorclass=DictCursor,
)
