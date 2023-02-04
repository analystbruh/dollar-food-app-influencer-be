from app import app
from flask import jsonify, request, make_response
import psycopg2 as pg
import os
from datetime import datetime as dt

dbname = os.environ['DOLLAR-FOOD-DB-NAME']
user = os.environ['DOLLAR-FOOD-DB-USERNAME']
password = os.environ['DOLLAR-FOOD-DB-PASSWORD']
host = os.environ['DOLLAR-FOOD-DB-HOST']

@app.route('/button-plays', methods=['POST','OPTIONS'])
def reviews():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers.add('Access-Control-Allow-Origin','*')
        res.headers.add('Access-Control-Allow-Headers','*')
        res.headers.add('Access-Control-Allow-Methods','*')
        return res
    elif request.method == 'POST':
        data = request.json
        if 'trackplay' not in data:
            query = """
                select
                    case
                        when extract(epoch from (now() - last_played)) < 86400
                        then 1
                        else 0
                    end
                from dfa_users
                where gtoken = %s
            """
            conn = pg.connect(dbname=dbname, user=user, password=password,  host=host)
            cursor = conn.cursor()
            cursor.execute(query,[data['user']])
            result = cursor.fetchall()
            if not result:
                cursor.execute('insert into dfa_users values (%s, null)', [data['user']])
                conn.commit()
                res = 0
            else:
                res = result[0][0]
            conn.close()
            res = jsonify(res)
            res.headers.add('Access-Control-Allow-Origin','*')
        else:
            conn = pg.connect(dbname=dbname, user=user, password=password,  host=host)
            cursor = conn.cursor()
            cursor.execute('update dfa_users set last_played=now() where gtoken = %s', [data['user']])
            conn.commit()
            conn.close()
            res = jsonify('success')
            res.headers.add('Access-Control-Allow-Origin','*')
        return res
