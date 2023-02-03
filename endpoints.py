from app import app
from flask import jsonify, request, make_response
import psycopg2

@app.route('/api/v1/reviews', methods=['GET','POST','OPTIONS'])
def reviews():
    if request.method == 'GET':
        data = request.args.to_dict()
        conn = psycopg2.connect('postgres://tmlvaqqwchhqhw:f28c92fafa959a28b6b8a94b6776538d581caab8ec95d679471b72d2b5163150@ec2-34-199-200-115.compute-1.amazonaws.com:5432/d1i53o5obnf90f')
        cursor = conn.cursor()
        cursor.execute(f'select * from dollar_reviews where restaurant = %s',[data.get('restaurant','NA')])
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        result_dict = [dict(zip(['id','restaurant','review','username', 'stars'], r)) for r in result]
        print(result_dict)
        res = jsonify(result_dict)
        res.headers.add('Access-Control-Allow-Origin','*')
        return res
    elif request.method == 'OPTIONS':
        res = make_response()
        res.headers.add('Access-Control-Allow-Origin','*')
        res.headers.add('Access-Control-Allow-Headers','*')
        res.headers.add('Access-Control-Allow-Methods','*')
        return res
    elif request.method == 'POST':
        data = request.json
        print(data)
        conn = psycopg2.connect('postgres://tmlvaqqwchhqhw:f28c92fafa959a28b6b8a94b6776538d581caab8ec95d679471b72d2b5163150@ec2-34-199-200-115.compute-1.amazonaws.com:5432/d1i53o5obnf90f')
        cursor = conn.cursor()
        cursor.execute('insert into dollar_reviews values (default,%s,%s,%s,%s)',[data['restaurant'], data['review'], data['username'], data['rating']])
        conn.commit()
        cursor.close()
        conn.close()
        res = jsonify('done')
        res.headers.add('Access-Control-Allow-Origin','*')
        return res
