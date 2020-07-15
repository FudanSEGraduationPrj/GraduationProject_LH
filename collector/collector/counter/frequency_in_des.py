from pymysql import *
import spacy
nlp = spacy.load('en_core_web_sm')

host = 'localhost'
port = 3306
user = 'root'
password = 'good2739966538'
database = 'api_explanation_extractor_db'
page_size = 100


def main():
    page_no = 1
    count = page_size
    # read 100 records from mysql each time
    while count >= page_size:
        conn = connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()
        count = cursor.execute('select description from explanation where id > %d limit %d' % ((page_no-1)*page_size, page_size))
        descriptions = cursor.fetchall()
        for des in descriptions:
            for token in nlp(des[0]):
                if token.is_alpha and not token.is_stop:
                    word = token.text.lower()
                    result = cursor.execute('select frequency from frequency where word = "%s"' % word)
                    if result == 0:
                        cursor.execute('insert into frequency VALUES ("%s", %d)' % (word, 1))
                        print("(word: %s, frequency: %d)" % (word, 1))
                    else:
                        c = cursor.fetchone()[0]
                        cursor.execute('update frequency set frequency = %d where word = "%s"' % (c+1, word))
                        print("(word: %s, frequency: %d)" % (word, c+1))
        conn.commit()
        conn.close()
        page_no += 1


if __name__ == '__main__':
    main()
