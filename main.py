import json
import pathlib

from db import connection

from flask import Flask, redirect, request, render_template, jsonify

app1 = Flask(__name__)

#RESTful api

@app1.route("/addresses/<int:retrieve_id>", methods=['GET'])
def get(retrieve_id):          #클라이언트에서 서버로 정보를 요청 -> 서버에서는 정보를 반환 // 조회
    data = retrieve_data(retrieve_id)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Not found'}), 404


@app1.route("/addresses", methods=['GET'])
def list_get():
    data = list_data()
    return jsonify(data)


@app1.route("/addresses", methods=['POST'])
def post():         #클라이언트에서 서버로 정보를 전달 -> 서버에서는 정보를 저장 // 삽입
    request_data = request.form
    insert_data(
        address=request_data['address'],
        owner_name=request_data['owner_name'],
        building_name=request_data['building_name'],
        number_of_people=request_data['number_of_people'],
        date_of_construction=request_data['date_of_construction']
    )
    return jsonify(last_data())



@app1.route("/addresses/<int:id>", methods=['PUT'])
def put(id):          #클라이언트에서 서버로 정보를 전달 -> 서버에서는 정보를 업데이트 // 수정
    request_data = request.form
    updated_data = modify_data(
        id=id,
        address=request_data['address'],
        owner_name=request_data['owner_name'],
        building_name=request_data['building_name'],
        number_of_people=request_data['number_of_people'],
        date_of_construction=request_data['date_of_construction']
    )
    if updated_data == -1:
        return jsonify({'error': '수정에 실패했습니다.'}), 400
    return jsonify(updated_data)


@app1.route("/addresses/<int:id>", methods=['DELETE'])
def delete(id):       #클라이언트에서 서버로 삭제 요청 -> 서버에서는 삭제 요청을 받고 정보 삭제 // 삭제
    exists = retrieve_data(id)
    if not exists:
        return jsonify({'error': '삭제 실패'}), 404

    delete_data(id)

    return jsonify({'success': '삭제 성공!'})

# 삽입 조회 수정 삭제

@app1.route("/")
def homepage():
    return render_template('homepage.html')

file_path = pathlib.Path(__file__).parent.resolve() / 'address_data.json'

address_data = []


def safety_int_input(label):
    value = None
    while True:
        value = input(label)
        if value.isdigit():
            return int(value)


def insert_data(address,
                owner_name,
                building_name,
                number_of_people,
                date_of_construction):
    with connection.cursor() as c:
        sql = f"""
                    INSERT INTO test_db1 (address, owner_name, building_name, number_of_people, date_of_construction)
                    VALUES ('{address}', '{owner_name}', '{building_name}', {number_of_people}, '{date_of_construction}');
                    """
        print('데이터 삽입 완료.')
        c.execute(sql)
        connection.commit()


def delete_data(id):
    with connection.cursor() as c:
        sql = f"""
            DELETE FROM test_db1 WHERE id = {id}
        """
        c.execute(sql)
        connection.commit()


def last_data():
    with connection.cursor() as c:
        c.execute("SELECT * FROM test_db1 ORDER BY id DESC LIMIT 1")
        return c.fetchone()


def retrieve_data(id):
    sql = f"""
    SELECT * FROM test_db1 WHERE id = {id}
    """
    with connection.cursor() as c:
        c.execute(sql)
        results = c.fetchone()
        if results:
            return results
        return None


def list_data():
    with connection.cursor() as c:
        c.execute("SELECT * FROM test_db1")
        return c.fetchall()


def modify_data(id,
                address,
                owner_name,
                building_name,
                number_of_people,
                date_of_construction):
    with connection.cursor() as c:
        c.execute(f"""
            SELECT * FROM test_db1 WHERE id = {id}
        """)
        original_data = c.fetchone()

        if not original_data:
            return -1

        original_data['address'] = address or original_data['address']
        original_data['owner_name'] = owner_name or original_data['owner_name']
        original_data['building_name'] = building_name or original_data['building_name']
        original_data['number_of_people'] = number_of_people or original_data['number_of_people']
        original_data['date_of_construction'] = date_of_construction or original_data['date_of_construction']

        c.execute(f"""
            UPDATE test_db1
            SET 
                address = '{address}',
                owner_name = '{owner_name}',
                building_name = '{building_name}',
                number_of_people = {number_of_people},
                date_of_construction = '{date_of_construction}'
            WHERE id = {id}
        """)
        connection.commit()
        return original_data



def save_file():
    with open(file_path, 'w') as f:
        json.dump(address_data, f, indent=4)


def call_file():
    with open("address_data.json", "r") as file:
        global address_data
        address_data = json.load(file)
