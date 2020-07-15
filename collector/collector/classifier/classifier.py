from keras.models import load_model
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from pymysql import *


model_path = 'model.h5'
model = load_model(model_path)

df = pd.read_csv('para_large.csv')
df.drop(['id'], axis=1, inplace=True)

tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
tokenizer.fit_on_texts(df.text)
vocab = tokenizer.word_index

host = 'localhost'
port = 3306
user = 'root'
password = 'good2739966538'
database = 'api_explanation_extractor_db'
page_size = 100



def main():
    # x = des
    # x = tokenizer.texts_to_sequences(x)
    # x = pad_sequences(x, maxlen=64)
    # is_explanation = np.argmax(model.predict(x), axis=1)[0]
    # print(is_explanation)
    page_no = 1
    count = page_size
    # read 100 records from mysql each time
    while count >= page_size:
        conn = connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()
        count = cursor.execute('select answer from answer where id > %d limit %d' % ((page_no - 1) * page_size, page_size))
        descriptions = cursor.fetchall()
        for des in descriptions:
            print(des)
            x = des
            x = tokenizer.texts_to_sequences(x)
            x = pad_sequences(x, maxlen=64)
            is_explanation = np.argmax(model.predict(x), axis=1)[0]
            if is_explanation == 1 and des[0].find("'") < 0:
                cursor.execute("update answer set is_explanation = 1 where answer = '%s'" % des[0])
        conn.commit()
        conn.close()
        page_no += 1


if __name__ == '__main__':
    main()
