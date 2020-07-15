from flask import Flask
from flask_cors import *
from pymysql import *
app = Flask(__name__)
CORS(app, supports_credentials=True)

host = '175.24.14.65'
port = 3306
user = 'root'
password = 'good2739966538'
database = 'api_explanation_extractor_db'


@app.route('/search/<words>', methods=['GET'])
def search(words):
    conn = connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()
    count = cursor.execute('select keyword, description from explanation where keyword like "%s"' % ('%' + words + '%'))
    descriptions = cursor.fetchall()
    results = {
        'results': []
    }
    for des in descriptions:
        result = {'keyword': des[0], 'description': des[1]}
        results['results'].append(result)
    conn.close()
    return results


@app.route('/hotword/all', methods=['GET'])
def all_hotword():
    conn = connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()
    count = cursor.execute('select words, degree from hotword order by degree desc limit 5')
    hotwords = cursor.fetchall()
    results = {
        'hotwords': []
    }
    for hotword in hotwords:
        result = {'text': hotword[0], 'degree': hotword[1]}
        results['hotwords'].append(result)
    conn.close()
    return results

@app.route('/hotword/degree/inc/<words>', methods=['POST'])
def inc_hotword_degree(words):
    conn = connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()
    count = cursor.execute('select degree from hotword where words = "%s"' % words)
    if count == 0:
        cursor.execute('insert into hotword (words, degree) VALUES ("%s", %d)' % (words, 1))
    else:
        degree = cursor.fetchone()[0]
        cursor.execute('update hotword set degree = %d where words = "%s"' % (degree+1, words))
    conn.commit()
    conn.close()
    return 'increase degree %s' % words


if __name__ == '__main__':
    app.run()
