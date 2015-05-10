#!env python
import random
import sys
import psycopg2

#Run with argv[1] == EC2 IP and argv[2] == # of records to insert.

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()
conn = psycopg2.connect(database="testdb", user="postgres", password="postgres", host=sys.argv[1], port=5432)
cur = conn.cursor()

cur.execute('DROP TABLE base;')

cur.execute('CREATE TABLE base (  first_name character varying(32) NOT NULL,  last_name character varying(32) NOT NULL,  cc character varying(16) NOT NULL );')

for x in range(int(sys.argv[2])):
    cc = random.randint(1000000000000000,9999999999999999);
    first = random.choice(WORDS)
    last = random.choice(WORDS)
    cur.execute("INSERT INTO base (first_name, last_name, cc) VALUES (%s, %s, %s)", (first, last, str(cc)))
    
conn.commit()
cur.close()
conn.close()

