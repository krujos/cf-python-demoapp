#!env python
from __future__ import print_function
from flask import Flask
from urlparse import urlparse

import json
import os
import sys
import psycopg2

lifecycle = None
creds = None
uri = None
if 'VCAP_SERVICES' in os.environ: 
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    lifecycle = vcap_services.get('lifecycle-sb') 
    if lifecycle is not None:
        creds = lifecycle[0].get('credentials') 
    if creds is not None:
        user = creds.get('username')
        password = creds.get('password') 
        uri = creds.get('uri') 
else:
    print ("VCAP_SERVICES not found!!!", file=sys.stderr)

port = 8003
if 'PORT' in os.environ: 
    port = int(os.getenv("PORT"))

Flask.get = lambda self, path: self.route(path, methods=['get'])

app = Flask(__name__)

@app.get('/')
def get_root(): 
    url = urlparse(uri)
    results = []
    output = "<p>Hello! Your db uri is <strong>%s</strong></p> " % url.geturl()
    try: 
        db = url.path.replace('/','')
        host = url.netloc.split(':')[0]
        conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=url.port)
        cur = conn.cursor()
        cur.execute('SELECT count(*) FROM base;')
        output += "<p>Table has %d rows</p>" % cur.fetchone()[0]
        cur.execute('SELECT * FROM base ORDER BY first_name DESC LIMIT 10;')
        output += "<table><thead><tr><td>First</td><td>Last</td><td>CC</td></thead>"
        for i in range(9):
            result = cur.fetchone()
            output += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (result[0], result[1], result[2])
        output += "</table>"

    except:
        print("ERR: Failed!", file=sys.stderr)
    
    return output;



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
