# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem
import spacy


# the pipeline used to filter newline character
class FilterNewlineCharacterPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # replace '\n' by ''
        if 'description' in item.keys():
            data = item['description']
            item['description'] = data.replace("\n", "")
        if 'text' in item.keys():
            data = item['text']
            item['text'] = data.replace("\n", "")
        if 'answer' in item.keys():
            data = item['answer']
            item['answer'] = data.replace("\n", "")
        return item


class StripPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # strip
        if 'description' in item.keys():
            data = item['description']
            item['description'] = data.strip()
        if 'text' in item.keys():
            data = item['text']
            item['text'] = data.strip()
        if 'answer' in item.keys():
            data = item['answer']
            item['answer'] = data.strip()
        return item


class FilterMultiSpacesPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # replace multi spaces by one
        if 'description' in item.keys():
            data = item['description']
            item['description'] = re.sub(r' +', ' ', data)
        if 'text' in item.keys():
            data = item['text']
            item['text'] = re.sub(r' +', ' ', data)
        if 'answer' in item.keys():
            data = item['answer']
            item['answer'] = re.sub(r' +', ' ', data)
        return item


nlp = spacy.load("en_core_web_sm")


class SyntaxAnalysisPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        result = ""
        data = "\n"
        if 'description' in item.keys():
            data = item['description']
        if 'text' in item.keys():
            data = item['text']
        if 'answer' in item.keys():
            data = item['answer']
        para = nlp(data)
        # divide paragraph into sentences
        for sent in para.sents:
            # dependency parsing
            desc = nlp(sent.text)
            hasSubject = False
            hasObject = False
            for token in desc:
                dep = token.dep_
                if (dep == 'expl') or (dep == 'csubj') or (dep == 'csubjpass') or (dep == 'nsubj') or (
                        dep == 'nsubjpass'):
                    hasSubject = True
                elif (dep == 'attr') or (dep == 'dobj') or (dep == 'pobj'):
                    hasObject = True
            if hasSubject and hasObject:
                result += sent.text
        if result == "":
            raise DropItem("illegal description")
        if 'description' in item.keys():
            item['description'] = result
        if 'text' in item.keys():
            item['text'] = result
        if 'answer' in item.keys():
            item['answer'] = result
        return item


from twisted.enterprise import adbapi


class MySQLPipeline(object):
    def open_spider(self, spider):
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('PORT', 3306)
        db = spider.settings.get('MYSQL_DB_NAME', 'api_explanation_extractor_db')
        user = spider.settings.get('MYSQL_USER', 'root')
        password = spider.settings.get('MYSQL_PASSWORD', 'good2739966538')
        # use connect pool to save resources
        self.conn_pool = adbapi.ConnectionPool('MySQLdb', host=host, port=port, db=db, user=user, password=password)

    def close_spider(self, spider):
        self.conn_pool.close()

    def process_item(self, item, spider):
        self.conn_pool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, transaction, item):
        if 'description' in item.keys():
            sql = 'INSERT INTO explanation (keyword, description) VALUES (%s, %s)'
            # (item['description',]) is a tuple, but (item['description']) is not a tuple
            # should use (item['description',]) otherwise there will be a bug
            transaction.execute(sql, (item['keyword'], item['description'].encode('utf-8')))
        if 'url' in item.keys():
            # used url_crc to accelerate the judgement process
            sql = 'SELECT * FROM url WHERE url_crc = crc32(%s) AND url = %s'
            if transaction.execute(sql, (item['url'], item['url'])) == 0:
                sql = 'INSERT INTO url (url, url_crc) VALUES (%s, crc32(%s))'
                transaction.execute(sql, (item['url'], item['url']))
        if 'text' in item.keys():
            sql = 'INSERT INTO para (is_explanation, text) VALUES (%s, %s)'
            transaction.execute(sql, (item['is_explanation'], item['text'].encode('utf-8')))
        if 'answer' in item.keys():
            sql = 'INSERT INTO answer (is_explanation, answer) VALUES (0, %s)'
            transaction.execute(sql, (item['answer'],))


from pymysql import *


class SimilarityPipeline(object):
    def open_spider(self, spider):
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('PORT', 3306)
        db = spider.settings.get('MYSQL_DB_NAME', 'api_explanation_extractor_db')
        user = spider.settings.get('MYSQL_USER', 'root')
        password = spider.settings.get('MYSQL_PASSWORD', 'good2739966538')
        self.vector_size = 100
        self.threshold = 0.05
        # read top 100 records from mysql
        conn = connect(host=host, port=port, user=user, password=password, database=db)
        cursor = conn.cursor()
        count = cursor.execute('select * from frequency order by frequency desc limit %d' % self.vector_size)

        # get vector
        self.words_1 = {}
        for kv in cursor.fetchall():
            word = kv[0]
            self.words_1[word] = kv[1]
        conn.commit()
        conn.close()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        words_2 = {}
        num = 0
        for token in nlp(item['description']):
            if token.is_alpha and not token.is_stop:
                word = token.text.lower()
                if word in words_2.keys():
                    words_2[word] = words_2[word] + 1
                else:
                    words_2[word] = 1
                num += 1
                if num >= self.vector_size:
                    break

        vector_1 = []
        vector_2 = []
        keys_1 = self.words_1.keys()
        keys_2 = words_2.keys()
        keys = list(keys_1)
        for key in keys_2:
            if key not in keys:
                keys.append(key)
        for key in keys:
            if key in keys_1:
                vector_1.append(self.words_1[key])
            else:
                vector_1.append(0)
            if key in keys_2:
                vector_2.append(words_2[key])
            else:
                vector_2.append(0)

        val_1 = 0
        val_2 = 0
        val_3 = 0
        for i in range(len(vector_1)):
            val_1 += vector_1[i] * vector_2[i]
            val_2 += vector_1[i] * vector_1[i]
            val_3 += vector_2[i] * vector_2[i]
        val_2 = val_2 ** 0.5
        val_3 = val_3 ** 0.5
        similarity = val_1 / (val_2 * val_3)
        print("similarity: %f" % similarity)
        if similarity < self.threshold:
            raise DropItem("Low Similarity")
        return item
