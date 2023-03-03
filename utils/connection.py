import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='031002',
    database='test_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
)
