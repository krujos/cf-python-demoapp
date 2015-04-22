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
    url = urlparse(uri.split("jdbc:")[-1])
    result = "-1"
    try: 
        db = url.path.replace('/','')
        host = url.netloc.split(':')[0]
        conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=url.port)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM touched;')
        result = cur.fetchone()[0]
    except:
        print("ERR: Failed!", file=sys.stderr)

    return "Hello! Your db uri is %s, it has been touched %s times." % (url.geturl(), result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
