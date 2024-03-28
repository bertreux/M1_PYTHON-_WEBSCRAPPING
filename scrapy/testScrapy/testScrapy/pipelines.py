# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class TestscrapyPipeline:
    def process_item(self, item, spider):
        return item

class SaveToMongoPipeline:

    def __init__(self):
        #connect to the MongoDB server (default is localhost on port 27017)
        self.conn = MongoClient('localhost', 27017)
        #access the database (create it if it doesn't exist)
        self.db = self.conn['quote_database']
        #access the collection (similar to a table in relational databases)
        self.collection = self.db['quote_collection']

    def process_item(self, item, spider):
        # Convert item to dict and insert into MongoDB
        self.collection.insert_one(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        #close the connection to the database
        self.conn.close()

import psycopg2
import json

class SavePostgreSQLPipeline:

    def __init__(self):
        # Connect to the PostgreSQL server
        # Update the connection details as per your PostgreSQL configuration
        self.conn = psycopg2.connect(
            host='localhost',
            dbname='postgres',
            user='postgres',
            password='fred'
        )
        self.cur = self.conn.cursor()

        # Create table if it doesn't exist
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            quote TEXT,
            author TEXT,
            about TEXT,
            tags JSONB
        )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        # Convert item to dict
        item_dict = ItemAdapter(item).asdict()

        # Insert data into the table
        self.cur.execute("""
        INSERT INTO quotes (quote, author, about, tags) VALUES (%s, %s, %s, %s)
        """, (item_dict['quote'], item_dict['author'], item_dict['about'], json.dumps(item_dict['tags'])))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Close the cursor and connection to the database
        self.cur.close()
        self.conn.close()